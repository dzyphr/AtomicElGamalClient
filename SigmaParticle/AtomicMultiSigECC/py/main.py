import secrets 
from jpype import *
import numpy as np
import hashlib
import ECC
from ECC import *
import os
import json
import base64
import time
import random
from dotenv import load_dotenv
import org.ergoplatform
import sigmastate
from sigmastate.interpreter.CryptoConstants import * 
from java.math import BigInteger
#from ergo_python_appkit.appkit import *
#from ergpy import helper_functions, appkit
import waits
import coinSelection
import scalaPipe
import sys
import ast
#ERGO ECC ADD point.add(point)
#ERGO ECC MULTIPLY G dlogGroup().generator().multiply(scalar) 
#[IN ERGOSCRIPT(on chain script) MULTIPLY IS Generator.exp(scalar)] because generator is GroupElement
def main(args):
    #Basic Variables
    curve = dlogGroup()
    n =  int(str(curve.order()))
    g = ECC.curve.g
    javaBigIntegerMAX = 57896044618658097711785492504343953926634992332820282019728792003956564819968
#    message = "1000000000" #some public change output #TODO:MAKE THIS MODULAR BEFORE PRODUCTION
    sha256 = hashlib.sha256()


    def p1Initiate(chainPubkey, localChain):
        if chainPubkey == "":
            print("enter chainPubkey as arg")
            exit(1)
        rs = random.randrange(0, n)
        rs = rs % n
        rs = rs % javaBigIntegerMAX
        rsERGO = BigInteger(str(rs))
        ks = random.randrange(0, n)
        ks = ks % n
        ks = ks % javaBigIntegerMAX
        ksERGO = BigInteger(str(ks))
        rsGERGO = dlogGroup().generator().multiply(rsERGO).normalize()
        ksG = scalar_mult(ks, g)
        ksGERGO = dlogGroup().generator().multiply(ksERGO).normalize()
        #return a JSON for easy cross lang/client parsing!
        p1InitiateOBJECT =  {
            "chainPubkey": chainPubkey,
            "localChain": localChain,
            "rsG": "(" + str(rsGERGO.getXCoord().toBigInteger()) + ", " + str(rsGERGO.getYCoord().toBigInteger()) + ")",
            "ksG": "(" + str(ksGERGO.getXCoord().toBigInteger()) + ", " + str(ksGERGO.getYCoord().toBigInteger()) + ")",
            "ks": ks, #must be stripped by client so it is not shared!
            "rs": rs #!!
        }
        return json.dumps(p1InitiateOBJECT, indent=4)

    def p2Response(ksGERGO, message, srFilePath, xFilePath):
        ksGERGO = ast.literal_eval(ksGERGO)
        ksGERGO_X = ksGERGO[0]
        ksGERGO_Y = ksGERGO[1]        
        ksGERGO = dlogGroup().curve().createPoint(BigInteger(str(ksGERGO_X)), BigInteger(str(ksGERGO_Y)))
        rr = random.randrange(0, n)
        rr = rr % n
        rr = rr % javaBigIntegerMAX
        rrERGO = BigInteger(str(rr))
        kr = random.randrange(0, n)
        kr = kr % n
        kr = kr % javaBigIntegerMAX
        krERGO = BigInteger(str(kr))
        krGERGO = dlogGroup().generator().multiply(krERGO).normalize()
    #    print("krGX-ERGO:", int(str(krGERGO.getXCoord().toBigInteger())), "krGY-ERGO:", int(str(krGERGO.getYCoord().toBigInteger())))
        krG = scalar_mult(kr, g)
        rrG = scalar_mult(rr, g)
        hashContent = message.encode() + str(ksGERGO.add(krGERGO)).encode()
        sha256.update(hashContent)
        e = int(sha256.digest().hex(), 16)
        e = e % n
        e = e % javaBigIntegerMAX
        eERGO = BigInteger(str(int(sha256.digest().hex(), 16)))
     #   print("e:", e)
        sr = kr + (e * rr)
        def gen_sr(kr, e, rr):
            sr = kr + (e * rr)
            sr = sr % n
            sr = sr % javaBigIntegerMAX
            while sr > javaBigIntegerMAX:
                rr = random.randrange(0, n)
                sr = kr + (e * rr)
                sr = sr % n
                sr = sr % javaBigIntegerMAX
                if sr < javaBigIntegerMAX:
                    return sr
                else: 
                    continue
            return sr 
        sr = gen_sr(kr, e, rr)
        srERGO = BigInteger(str(sr))
        f = open(srFilePath, "w")
        f.write(str(srERGO))
        f.close()
      #  print("\np2 creates their multisig value sr:", sr)
        x = secrets.randbits(256)
        x = x % n
        x = x % javaBigIntegerMAX
        f = open(xFilePath, "w")
        f.write(str(x))
        f.close()
        xERGO = BigInteger(str(x))
       # print("\np2 creates a 256bit secret preimage x:", x)
        xGERGO = dlogGroup().generator().multiply(xERGO).normalize()
       # print("xGERGO:", xGERGO)
        srGERGO = dlogGroup().generator().multiply(srERGO).normalize()#sr is on ERGO
        srG = scalar_mult(sr, g)
        xG = scalar_mult(x, g)#x is on EVM chain
       # print("srGX-ERGO:", int(str(srGERGO.getXCoord().toBigInteger())), "srGY-ERGO:", int(str(srGERGO.getYCoord().toBigInteger())))
       # print("\np2 multiplies the preimage by secp256k1 generator G to get xG:", xG)
        sr_ = sr + x
        sr_ = sr_  
       # print("\np2 computes a partial equation for p1 sr_ = sr - x. \n\nsr_:", sr_)
       # print("\np2 sends sr_ and xG along with srG to p1")
        p2RespondOBJECT = {
                "sr_": str(sr_),
                "xG": str(xG),
                "srG": "(" + str(srGERGO.getXCoord().toBigInteger()) + ", " + str(srGERGO.getYCoord().toBigInteger()) + ")",
                "krG": "(" + str(krGERGO.getXCoord().toBigInteger())  + ", " + str(krGERGO.getYCoord().toBigInteger()) + ")",
                "e": str(e) #TODO:figure out if Ergo specific e is necessary above
                #TODO: make chain specific
        }
        return json.dumps(p2RespondOBJECT, indent=4)

    def p1Finalize(sr_, xG, srG,  e, ks, rs):
        sr_ = int(sr_)
        e = int(e)
        rs = int(rs)
        ks = int(ks)
        xG = ast.literal_eval(xG)
        srG = ast.literal_eval(srG)

        check = add_points(srG, xG) #P1 CHECKS WITH ECC
        sr_G = scalar_mult(sr_, g)
        #print("\np1 checks that srG + xG == sr_G", check, "==", sr_G, "and that xG are locking funds in contract")
        assert(check == sr_G)
        #print("\np1 locks funds to contract that checks that the inputed sr and ss are == to srG and ssG as well as include krG and ksG in the second half of the conditions")
        ss = ks + e * rs
        ss = ss % n
        ss = ss % javaBigIntegerMAX
        ssERGO = BigInteger(str(ss))
        ssGERGO = dlogGroup().generator().multiply(ssERGO).normalize()
        finalSignatureObject = {
                "ss":  str(ssERGO),
                "ssG": "(" + str(ssGERGO.getXCoord().toBigInteger())  + ", " + str(ssGERGO.getYCoord().toBigInteger()) + ")"
        }
        return json.dumps(finalSignatureObject, indent=4)
        #print("create ergo script locked to ", srGERGO, ssGERGO, krGERGO, ksGERGO)
        #print("\np1 computes their part of the signature ss = ks + e * rs:", ss, "and sends result to p2" )
    #    print("ss:", ss, "ssGERGO", ssGERGO)
        #print("ssGX-ERGO:", int(str(ssGERGO.getXCoord().toBigInteger())), "ssGY-ERGO:", int(str(ssGERGO.getYCoord().toBigInteger())))
        #print("\np2 computes their part of the signature sr = kr + e * rr:", sr)
        #Q = sr + ss
        #print("\nthe contract can check for the combined sig:", Q, "obtained by doing assert([input]ss*G + sr*G == [spending condition]ssG + srG)")



        #print("\np1 sees that p2 broadcasted Q on chain and can then use it to compute sr")

        #p1sr = Q - ss
        #print("\nsr:", sr,"==", "p1sr:", p1sr)
        #assert(sr == p1sr )
    def p1Deduce(sr_, sr):
        p1x = int(sr_) - int(sr)  #p1 discovers x this way
        xObj = {
            "x": str(p1x)
        }
        return json.dumps(xObj, indent=4)
        #print("p1 can now spend value locked to hash/public pair xG with x and their signature")

#    def test():

    if len(args) > 1:
        command = args[1]
        if command == "p1Initiate":
            if len(args) > 2:
                if len(args) > 3:
                    sys.stdout.write(str(p1Initiate(args[2], args[3])))
                else:
                    print("enter your local chain  as following arg")
            else:
                print("enter chainPubkey as following arg")
        if command == "p2Respond":
            if len(args) > 3:
               sys.stdout.write(str(p2Response(args[2], args[3], args[4], args[5])))
            else:
                print("enter ksG, Message, srFilePath, and xFilePath as following args")
        if command == "p1Finalize":
            if len(args) > 4:
                sys.stdout.write(str(p1Finalize(args[2], args[3], args[4], args[5], args[6], args[7])))
            else:
                print("enter:\n sr_, xG, srG, e \nas followup arguments")
        if command == "p1Deduce":
            if len(args) > 3:
                sys.stdout.write(str(p1Deduce(args[2], args[3])))
            else:
                print("enter sr_ and sr as followup arguments")
#        else:
#            test()
    


    '''
    check = add_points(srG, xG) #P1 CHECKS WITH ECC
    sr_G = scalar_mult(sr_, g)
    print("\np1 checks that srG + xG == sr_G", check, "==", sr_G, "and that xG are locking funds in contract")
    assert(check == sr_G, "check != sr_G")
    print("\np1 locks funds to contract that checks that the inputed sr and ss are == to srG and ssG as well as include krG and ksG in the second half of the conditions")
    ss = ks + e * rs
    ss = ss % n
    ss = ss % javaBigIntegerMAX
    ssERGO = BigInteger(str(ss))
    ssGERGO = dlogGroup().generator().multiply(ssERGO).normalize()
    print("create ergo script locked to ", srGERGO, ssGERGO, krGERGO, ksGERGO)
    print("\np1 computes their part of the signature ss = ks + e * rs:", ss, "and sends result to p2" )
#    print("ss:", ss, "ssGERGO", ssGERGO)
    print("ssGX-ERGO:", int(str(ssGERGO.getXCoord().toBigInteger())), "ssGY-ERGO:", int(str(ssGERGO.getYCoord().toBigInteger())))
    print("\np2 computes their part of the signature sr = kr + e *rr:", sr)
    Q = sr + ss
    print("\nthe contract can check for the combined sig:", Q, "obtained by doing assert([input]ss*G + sr*G == [spending condition]ssG + srG)")
    print("\np1 sees that p2 broadcasted Q on chain and can then use it to compute sr")
    p1sr = Q - ss
    print("\nsr:", sr,"==", "p1sr:", p1sr)
    assert(sr == p1sr )
    p1x = sr_ - sr  #p1 discovers x this way
    print("\np1 discovers sr_ - sr = x", p1x)
    assert(p1x == x)
    print("p1 can now spend value locked to hash/public pair xG with x and their signature")






    ''' 


























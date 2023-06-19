from datetime import datetime
import ast
import subprocess
from GUI_manager import *
from chain import setLocalChainPubkeyManual, setCrossChainPubkeyManual, setCrossChainPubkeyDerived
import tkinter, customtkinter, os, json, time, subprocess, sys, io, pyperclip
from tools import *
def initiatorStart(self): #initiator operation #start operations should not have update  functions at the beginning
                            #because they imply newly generated content
                            #update functions imply already generated content
    self.currentswapname = determineSwapName()
    if self.chainPubkey == "":
        setCrossChainPubkeyManual(self)
    init = "python3 -u SigmaParticle/AtomicMultiSigECC/py/deploy.py  p1Initiate " + self.chainPubkey + " " + self.initiatorChain
    initiation = os.popen(init).read() #run wit -u for unbuffered stream
    j = json.loads(initiation)
    ks = j["ks"]
    rs = j["rs"]
    strippedInitiation = initiation.replace("\"ks\": " + str(ks) + ",", "")
    strippedInitiation1 = strippedInitiation.replace("\"rs\": " + str(rs) , "")
    #extra redundant cases: (if json order changes)
    strippedInitiation2 = strippedInitiation1.replace("\"rs\": " + str(rs) + ",", "")
    strippedInitiation3 = strippedInitiation2.replace("\"ks\": " + str(ks), "")
    #redundant cases implemented in case of json protocol change prevents secret leakage
    ksG = j["ksG"]
    #get rid of last comma and newlines
    strippedInitiation4 = strippedInitiation3.replace("\"ksG\": \"" + str(ksG) + "\",", "\"ksG\": \"" + str(ksG) + "\"")
    strippedInitiation5 = strippedInitiation4.replace("}", "")
    strippedInitiation5.rstrip()
    strippedInitiation6 = strippedInitiation5.replace("\"ksG\": \"" + str(ksG) + "\"", "\"ksG\": \"" + str(ksG) + "\"\n}")
#    print(strippedInitiation6)
    #STRIP ks AND rs !!!!
    #save non stripped version to PRIVATE labeled file
    #proceed normally with stripped version
    #obviously strip BEFORE encryption
    runElGamal = "./ElGamal encryptToPubKey " + \
            self.currentReceiver + ' ' + \
            self.ElGamalKeyFileName + ' ' + \
            "\'" + strippedInitiation6 + "\' " + \
            self.currentswapname + "/ENC_initiation.atomicswap "
    encryption = os.popen(runElGamal).read()
    f = open(self.currentswapname + "/PRIV_initiation.atomicswap", "w")
    f.write(initiation)
    f.close()
    f = open(self.currentswapname + "/initiation.atomicswap", "w")
    f.write(strippedInitiation6)
    f.close()
    f = open(self.currentswapname + "/Receiver.ElGamalPub", "w")
    f.write(self.currentReceiver)
    f.close()
    f = open(self.currentswapname + "/SenderKey.ElGamalPub", "w")
    #maybe we can just backup the whole private keyfile in this instance
    f.write(self.ElGamalPublicKey)
    f.close()
    if self.swapTabSet == False:
        setSwapTab(self, True)
    else:
        setSwapTab(self, False)


def copyENCInit(self):
    updateDataBasedOnOpenTab(self)
    pyperclip.copy(open(self.swap_tab_view.get() + "/ENC_initiation.atomicswap", "r").read())
    self.swap_tab_view.decryptResponderCommitmentButton.configure(state="normal")

    #make sure active tab functions get swap name from current open tab

def inspectScalarLockContract(self): #initiator operation
    updateDataBasedOnOpenTab(self)
    decryptResponse(self)
    f = open(self.currentswapname + "/DEC_response.atomicswap", "r")
    j = json.loads(f.read())
    f.close()
    chain = j["chain"]
    contractAddr = j["contractAddr"]
    if chain == "Goerli":
        self.scalarContractFundingAmount = os.popen("cd Atomicity/Goerli && python3 -u py/deploy.py " + contractAddr).read()
    elif chain == "Sepolia":
        self.scalarContractFundingAmount = os.popen("cd Atomicity/Sepolia && python3 -u py/deploy.py getBalance " + contractAddr).read()
    self.swap_tab_view.responderContractValueLabel.configure(text= "Responder Contract Value: " +\
            self.scalarContractFundingAmount + " wei")
    if int(self.scalarContractFundingAmount) > 0:
        self.swap_tab_view.finalizeSwapButton.configure(state="normal")
    print(self.scalarContractFundingAmount)



def decryptResponse(self): #initiator operation
    updateDataBasedOnOpenTab(self)
    if os.path.isfile(self.currentswapname + "/response.atomicswap"):
        print("response commitment already collected for ", self.currentswapname)
    else:
        if self.swap_tab_view.responderCommitment.get() != "":
            responseFile = open(self.currentswapname + "/response.atomicswap", "w")
            responseFile.write(self.swap_tab_view.responderCommitment.get())
            decryptElGamal = \
                        "./ElGamal decryptFromPubKey " + self.currentswapname + "/response.atomicswap " + \
                        self.currentReceiver + ' ' + self.ElGamalKeyFileName
            decrypt = os.popen(decryptElGamal).read()
            f = open(self.currentswapname + "/DEC_response.atomicswap", "w")
            f.write(decrypt)
            f.close()
            print(decrypt)
        else:
            print("enter the commitment from responder!")


def draftFinalSignature(self): #create the final sig ss and pub value sG #initiator operation
    if os.path.isfile(self.currentswapname + "/finalize.atomicswap") == False or os.path.isfile("SigmaParticle/" + self.currentswapname + "/boxId") == False:
        updateDataBasedOnOpenTab(self)
        if int(self.swap_tab_view.initiatorContractValueEntry.get()) >= 123841:
            f = open(self.currentswapname + "/DEC_response.atomicswap", "r")
            j = json.loads(f.read())
            f.close()
            sr_ = j["sr_"]
            xG = j["xG"]
            srG = j["srG"]
            e = j["e"]
            f = open(self.currentswapname + "/PRIV_initiation.atomicswap", "r")
            j = json.loads(f.read())
            f.close()
            ks = j["ks"]
            rs = j["rs"]
            cmd = "cd SigmaParticle/AtomicMultiSigECC/ && python3 -u py/deploy.py p1Finalize " + \
                    "\"" + str(sr_) + "\"" + " \"" + xG.replace(" ", "") + "\" \"" + srG.replace(" ", "") + "\" \"" + str(e) + "\" " + \
                    "\"" + str(ks) + "\"" + " \"" + str(rs) + "\""
            finalSigJson = os.popen(cmd).read()
            if json.loads(finalSigJson) != ValueError and finalSigJson != "":
                print(finalSigJson)
                f = open(self.currentswapname + "/finalize.atomicswap", "w")
                f.write(finalSigJson)
                f.close()
                SigmaParticleAtomicSchnorr(self)
                time.sleep(3)
                f = open(self.currentswapname + "/finalize.atomicswap", "w")
                f2 = open("SigmaParticle/" + self.currentswapname + "/boxId", "r")
                boxId = f2.read()
                f2.close()

                mod = finalSigJson
                modified = mod.replace("\"\n}", "\",\n    \"boxId\": \"" + boxId + "\"\n}")
                print(modified)
                f.write(modified)
                f.close()
                cmd = \
                    "./ElGamal encryptToPubKey " + \
                    self.currentReceiver + ' ' + \
                    self.ElGamalKeyFileName + ' ' + \
                    "\'" + modified + "\' " + \
                    self.currentswapname + "/ENC_finalize.atomicswap"
                encrypt = os.popen(cmd).read()
                f = open(self.currentswapname + "/ENC_finalize.atomicswap", "r")
                encryption = f.read()
                f.close()
                #now upload ergoscript contract
                pyperclip.copy(encryption)
                self.swap_tab_view.finalizeCheck.configure(state="normal")
        else:
            print("you must spend minimum 123841 nanoErg into the contract or else it is unclaimable!")


    if os.path.isfile("SigmaParticle/" + self.currentswapname + "/boxId") == True: #if we already have the box we have properly uploaded the contract
        f = open(self.currentswapname + "/ENC_finalize.atomicswap", "r")
        encryption = f.read()
        f.close()
        pyperclip.copy(encryption)

def checkTreeForFinalization(self):
    updateDataBasedOnOpenTab(self)
    f = open("SigmaParticle/" + self.currentswapname + "/ergoTree")
    tree = f.read()
    f.close()
    f = open(self.currentswapname + "/finalize.atomicswap")
    j = json.loads(f.read())
    f.close()
    boxId = j["boxId"]
    treeToAddrCmd = \
            "cd SigmaParticle/treeToAddr && ./deploy.sh " + tree
    addr = json.loads(os.popen(treeToAddrCmd).read())["address"]
    print("addr: ", addr)
    boxFilterCmd =\
            "cd SigmaParticle/boxFilter &&" +\
            "./deploy.sh " + addr + " " + boxId + " ../../" + self.currentswapname + "/atomicClaim"
    print(os.popen(boxFilterCmd).read())
    if os.path.isfile(self.currentswapname + "/atomicClaim_tx1"):
        f = open(self.currentswapname + "/atomicClaim_tx1", "r")
        j = json.loads(f.read())
        f.close()
        R4 = j["outputs"][0]["additionalRegisters"]["R4"]
        f = open(self.currentswapname + "/sr", "w")
        f.write(R4)
        f.close()
        self.swap_tab_view.claim.configure(state="normal")
    else:
        print("no atomic claim transactions found")


def deduce_sr(self):
    updateDataBasedOnOpenTab(self)
    f = open(self.currentswapname + "/DEC_response.atomicswap", "r")
    j = json.loads(f.read())
    sr_ = j["sr_"]
    contractAddr = j["contractAddr"]
    chain = j["chain"]
    f.close()
    f = open(self.currentswapname + "/sr", "r")
    sr = f.read()
    f.close()
    decodeCMD = \
            "cd SigmaParticle/valFromHex && ./deploy.sh " + sr + " ../../" + self.currentswapname + "/decoded_sr"
    decodeResponse = os.popen(decodeCMD).read()
    f = open(self.currentswapname + "/decoded_sr", "r")
    dec_sr = f.read()
    f.close()
    deduceCMD = \
            "cd SigmaParticle/AtomicMultiSigECC && python3 -u py/deploy.py p1Deduce " + sr_ + " " + dec_sr
    #note when we do python operations and want to capture the output as json we should not run the deploy.sh but call python3
    response = os.popen(deduceCMD).read()
    j = json.loads(response)
    x = j["x"]
    gas = self.swap_tab_view.InitiatorGasEntry.get()
    gasMod = self.swap_tab_view.InitiatorGasModEntry.get()
    claimScript = \
                "cd Atomicity/" + chain + " && ./deploy.sh claim " + contractAddr + " " + x + " " + gas + " " + gasMod
    print(claimScript)
    print(os.popen(claimScript).read())

def deploySigmaParticleAtomicSchorr(self):
    command = "cd SigmaParticle/" + self.currentswapname + " && ./deploy.sh deposit"
    devnull = open(os.devnull, 'wb')
    response = subprocess.Popen(command, shell=True,
                         stdout=devnull, stderr=devnull,
                         close_fds=True)


def SigmaParticleAtomicSchnorr(self):
    updateDataBasedOnOpenTab(self)
    f = open(self.currentswapname + "/DEC_response.atomicswap", "r")
    response = f.read()
    f.close()
    j = json.loads(response)
    krG = ast.literal_eval(j["krG"])
    srG = ast.literal_eval(j["srG"])
    f = open(self.currentswapname + "/finalize.atomicswap", "r")
    finalize = f.read()
    f.close()
    j = json.loads(finalize)
    ssG = ast.literal_eval(j["ssG"])
    f = open(self.currentswapname + "/initiation.atomicswap", "r")
    j = json.loads(f.read())
    ksG = ast.literal_eval(j["ksG"])
    f = open(self.currentswapname + "/DEC_response.atomicswap", "r")
    j = json.loads(f.read())
    f.close()
    receiver = j[self.initiatorChain + "_chainPubkey"]
    if self.swap_tab_view.refundDurationEntry.get() == "":
        refundDuration = 25
    else:
        refundDuration = self.swap_tab_view.refundDurationEntry.get()
    cmd = "cd SigmaParticle && ./new_frame " + str(self.currentswapname) + \
            " && cd " + str(self.currentswapname) + " && echo " + \
            "'" + \
            "senderEIP3Secret=" + self.chainPubkeyEntry.get()  + "\n" + \
            "receiverAddr=\"" + receiver + "\"\n" + \
            "ergoAmount=" + str(self.swap_tab_view.initiatorContractValueEntry.get()) + "\n" +\
            "refundDuration=" + str(refundDuration) + "\n" + \
            "krGX=" + str(krG[0]) + "\n" +\
            "krGY=" + str(krG[1]) + "\n" +\
            "ksGX=" + str(ksG[0]) + "\n" +\
            "ksGY=" + str(ksG[1]) + "\n" +\
            "srGX=" + str(srG[0]) + "\n" +\
            "srGY=" + str(srG[1]) + "\n" +\
            "ssGX=" + str(ssG[0]) + "\n" +\
            "ssGY=" + str(ssG[1]) + "\n" +\
            "'" + \
            " >> .env"
    createContractFolder = os.popen(cmd).read()
    copyScriptsCommand = "cp SigmaParticle/AtomicMultiSig/py/main.py SigmaParticle/" + self.currentswapname + "/py/main.py"
    copyScripts = os.popen(copyScriptsCommand).read()
    deploySigmaParticleAtomicSchorr(self)
    self.swap_tab_view.checkRefundLockTime.configure(state="normal")


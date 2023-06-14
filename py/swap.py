from datetime import datetime
import ast
import subprocess
from GUI_manager import *
from chain import setLocalChainPubkeyManual, setCrossChainPubkeyManual, setCrossChainPubkeyDerived
import tkinter, customtkinter, os, json, time, subprocess, sys, io, pyperclip

class SwapTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

def updateDataBasedOnOpenTab(self):
    if hasattr(self, "swap_tab_view"):
        self.currentswapname = self.swap_tab_view.get()
    '''
    if os.isdir(openTabSwapName) == True:
        #roledata
        f = open(openTabSwapName + "/roleData.json", "r")
        role = f.read()
        f.close()
        if role == "initiator":
            self.isInitiator == True
        elif role == "responder":
            self.isInitiator == False
        #swapname
        self.currentswapname = openTabSwapName
        #chainpubkey
    '''

def saveRole(self):
    if self.isInitiator == True:
        f = open(self.currentswapname + "/roleData.json", "w")
        f.write("{\n" + 
                "    \"role\": \"initiator\"\n" +
                "}")
        f.close()
    else:
        f = open(self.currentswapname + "/roleData.json", "w")
        f.write("{\n" +
                "    \"role\": \"responder\"\n" +
                "}")
        f.close()

def setInitiator(self): #here we are setting the initiator based on the PREVIOUS state of the isInitiator boolean
    if self.isInitiator == True:
        self.isInitiator = False
        print("isInitiator = ", self.isInitiator)
        GUI_Arrange_Swap_Based(self)
        GUI_ReArrange_Chain_Based(self)
    else:
        self.isInitiator = True
        print("isInitiator = ", self.isInitiator)
        GUI_Arrange_Swap_Based(self)
        GUI_ReArrange_Chain_Based(self)

def determineSwapName():
    swap = "swap"
    index = 1
    strindex = str(index)
    swapname = swap + strindex
    if os.path.isdir(swapname) == False:
        print(swapname + " dir not found")
        os.mkdir(swapname)
    else:
        while True:
            index = index + 1
            strindex = str(index)
            swapname = swap + strindex
            if os.path.isdir(swapname) == False:
                os.mkdir(swapname)
                print("making dir " + swapname )
                break
    return swapname

def copyENCInit(self):
    updateDataBasedOnOpenTab(self)
    pyperclip.copy(open(self.swap_tab_view.get() + "/ENC_initiation.atomicswap", "r").read())
    self.swap_tab_view.decryptResponderCommitmentButton.configure(state="normal")

    #make sure active tab functions get swap name from current open tab

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

            



def deploySigmaParticleAtomicSchorr(self):
    command = "cd SigmaParticle/" + self.currentswapname + " && ./deploy.sh deposit"
    devnull = open(os.devnull, 'wb')
    response = subprocess.Popen(command, shell=True,
                         stdout=devnull, stderr=devnull,
                         close_fds=True)
#   print(response)
#   if "404" not in response:
#        self.swap_tab_view.finalizeCheck.configure(state="normal")
    #response should already be a json minus initial "Running ..." Statement


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


def nanoErgToErgo(nanoErgs): #only for round amounts
    return int(int(nanoErgs) / 1000000000)

def receiverClaim(self):
    updateDataBasedOnOpenTab(self)
    if os.path.isfile(self.currentswapname + "/ENC_Finalization.atomicswap") == False:
        print("finalization not found! paste in finalization and check contract value first!")
    else:
        newContractCmd = "cd SigmaParticle && ./new_frame " + self.currentswapname
        print(os.popen(newContractCmd).read())
        copyBoilerplateCmd = "cp SigmaParticle/AtomicMultiSig/py/main.py SigmaParticle/" + self.currentswapname  + "/py/main.py"
        print(os.popen(copyBoilerplateCmd).read())
        f = open(self.currentswapname + "/sr")
        sr = f.read()
        f.close()
        f = open(self.currentswapname + "/DEC_Finalization.atomicswap", "r")
        j = json.loads(f.read())
        f.close()
        ss = j["ss"]
        f = open(self.currentswapname + "/DEC_initiation.atomicswap")
        ksG = json.loads(f.read())["ksG"]
        f.close()
        f = open(self.currentswapname + "/response_commitment.atomicswap")
        krG = json.loads(f.read())["krG"]
        f = open(self.currentswapname + "/DEC_Finalization.atomicswap", "r")
        j = json.loads(f.read())
        f.close()
        boxId = j["boxId"]
        f = open(self.currentswapname + "/InitiatorContractValue")
        nanoErgs = f.read()
        f.close()
        echoVariablesCMD = \
                "echo \"" + \
                "sr=" + sr + "\n" + \
                "ss=" + ss + "\n" + \
                "ksGX=" + str(ast.literal_eval(ksG)[0]) + "\n" + \
                "ksGY=" + str(ast.literal_eval(ksG)[1]) + "\n" + \
                "krGX=" + str(ast.literal_eval(krG)[0]) + "\n" + \
                "krGY=" + str(ast.literal_eval(krG)[1]) + "\n" + \
                "atomicBox=" + "\"" + boxId + "\"\n" + \
                "ergoAmount=" + str(nanoErgs) + "\n" + \
                "\" >> SigmaParticle/" + self.currentswapname + "/.env"
        print(os.popen(echoVariablesCMD).read())
        claimCMD = \
                "cd SigmaParticle/" + self.currentswapname + " && ./deploy.sh claim"
        print(os.popen(claimCMD).read())


def receiverCheck(self): #responder operatio
    updateDataBasedOnOpenTab(self)
    if self.swap_tab_view.finalizeEntry.get() == "":
        print("paste in the finalization to claim!")
    else:
        ENCFin = self.swap_tab_view.finalizeEntry.get()
        f = open(self.currentswapname + "/ENC_Finalization.atomicswap", "w")
        f.write(ENCFin)
        f.close()
        decryptElGamal = \
            "./ElGamal decryptFromPubKey " + self.currentswapname + "/ENC_Finalization.atomicswap " + \
            self.currentReceiver + ' ' + self.ElGamalKeyFileName
        decryption = os.popen(decryptElGamal).read()
        f = open(self.currentswapname + "/DEC_Finalization.atomicswap", "w")
        f.write(decryption)
        f.close()
        j = json.loads(decryption)
        boxValCheck = "cd SigmaParticle/boxValue && ./deploy.sh " +\
                j["boxId"] + " ../../" +\
                self.currentswapname + "/InitiatorContractValue"
        devnull = open(os.devnull, 'wb') 
        
#       os.popen(boxValCheck)
        p = subprocess.Popen(boxValCheck, shell=True,
                         stdout=devnull, stderr=devnull,
                         close_fds=True)
        if os.path.isfile(self.currentswapname + "/InitiatorContractValue") == True:
            f = open(self.currentswapname + "/InitiatorContractValue")
            nanoErgs = f.read()
            f.close()
            if int(nanoErgs) < 123841:
                print("box is extremely small dust and may not be able to be properly claimed")
                self.swap_tab_view.labelContractAmount.configure(text= "Contract Value: " +\
                    "potentially unspendable dust")
            else:
                self.swap_tab_view.labelContractAmount.configure(text= "Contract Value: " +\
                    nanoErgs + " nΣ")
                self.swap_tab_view.claimButton.configure(state="normal")
        else:
            print("cant find box, tx not mined yet or invalid id")

def SigmaParticleRefund(self):
    updateDataBasedOnOpenTab(self)
    devnull = open(os.devnull, 'wb')
    f = open("SigmaParticle/" + self.currentswapname + "/boxId", "r")
    boxId = f.read()
    f.close()
    echoBoxIdCMD = \
            "echo '\natomicBox=" + boxId + "' >> SigmaParticle/" + self.currentswapname + "/.env"
    os.popen(echoBoxIdCMD).read()

    cmd =  "cd SigmaParticle/" + self.currentswapname + "&& ./deploy.sh refund"
    os.popen(cmd).read()

def getLocalLockTime(self): #for refunds #returns lock time in # of blocks
    updateDataBasedOnOpenTab(self)
    f = open(self.currentswapname + "/roleData.json", "r") #TODO: This is likely the most accurate way to pick a chain responsively
    role = json.loads(f.read())["role"]
    f.close()
    if role == "initiator":
        f = open(self.currentswapname + "/initiation.atomicswap", "r")
        initiatorChain = json.loads(f.read())["localChain"]
        f.close()
        if initiatorChain == "Ergo":
            f = open("SigmaParticle/" + self.currentswapname + "/boxId", "r")
            boxId = f.read()
            f.close()
            lockHeightCMD = \
                            "cd SigmaParticle/boxConstantByIndex && ./deploy.sh " + boxId + \
                            " 7 ../../" + self.currentswapname + "/localChain_lockHeight"
            os.popen(lockHeightCMD).read()
            currentHeightCMD = \
                            "cd SigmaParticle/currentHeight && ./deploy.sh ../../" + \
                            self.currentswapname + "/localChain_currentHeight"
            os.popen(currentHeightCMD).read()
            f = open(self.currentswapname + "/localChain_lockHeight")
            lockHeight = f.read()
            f.close()
            f = open(self.currentswapname + "/localChain_currentHeight")
            currentHeight = f.read()
            f.close()
            if int(currentHeight) <= int(lockHeight):
                return int(lockHeight) - int(currentHeight) + 1 #plus 1 because currently contract checks for GREATER THAN lock height
            else:
                return 0
    if role == "responder":
        f = open(self.currentswapname + "/response_commitment.atomicswap", "r")
        responderChain = json.loads(f.read())["chain"]
        f.close()
        if responderChain == "Sepolia":
            f = open(self.currentswapname + "/response_commitment.atomicswap", "r")
            addr = json.loads(f.read())["contractAddr"]
            f.close()
#            print("todo checklocktime function made of check timelock and current lock time math in Atomicity script")
            cmd = \
                    "cd Atomicity/" + self.currentswapname + " && ./deploy.sh lockTime " + \
                    addr + " ../../" + self.currentswapname + "/remainingLockTime"
            print(cmd)
            os.popen(cmd).read()
            if os.path.isfile(self.currentswapname + "/remainingLockTime"):
                f = open(self.currentswapname + "/remainingLockTime", "r")
                lockTime = f.read()
                f.close()
                return lockTime
            else:
                print("failed to create or find remainingLockTime file")
        


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
#               currentHeightCMD = \
#                       "cd SigmaParticle/currentHeight && ./deploy.sh ../../" + self.currentswapname + "/localChain_currentHeight"
#                os.popen(currentHeightCMD).read()
                time.sleep(3)
                f = open(self.currentswapname + "/finalize.atomicswap", "w")
                f2 = open("SigmaParticle/" + self.currentswapname + "/boxId", "r") 
                boxId = f2.read()
                f2.close()
#                lockHeightCMD = \
#                        "cd SigmaParticle/boxConstantByIndex && ./deploy.sh " + boxId + \
#                        " ../../" + self.currentswapname + "/localChain_lockHeight"
#                os.popen(lockHeightCMD).read()

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

def initiatorStart(self): #initiator operation
    updateDataBasedOnOpenTab(self)
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

def copyResponse(self): #esponder operation
    updateDataBasedOnOpenTab(self)
    if os.path.isfile(self.currentswapname + "/responderContractAddress"):
        if os.path.isfile(self.swap_tab_view.get() + "/response_commitment.atomicswap"):
            addr = open(self.currentswapname + "/responderContractAddress", "r").read().rstrip()
            response = open(self.swap_tab_view.get() + "/response_commitment.atomicswap", "r").read()
            if "chain" not in response :
                f = open(self.currentswapname + "/response_commitment.atomicswap", "w")
                init = open(self.currentswapname + "/DEC_initiation.atomicswap", "r").read()
                j = json.loads(init)
                self.counterpartyChainPubkey = j["chainPubkey"]
                self.crossChain = j["localChain"]
                if self.crossChain == "Ergo": #TODO: any non account chain
                    if self.chainPubkeyEntry.get() == "":
                        self.chainPubkeyEntry.insert(0, "0")
                        print("pubkey index not specified using 0")
                setCrossChainPubkeyDerived(self)
                GUI_ReArrange_Chain_Based(self)
                edit = response.replace(\
                        "\n}", \
                        ",\n" + 
                        "    \"contractAddr\": " + "\"" + addr.rstrip() + "\"" + ",\n"  + \
                        "    \"chain\": " + "\"" + self.responderChain.rstrip() + "\"" + ",\n" + \
                        "    \"" + self.crossChain  + "_chainPubkey\": " + "\"" + self.chainPubkey.rstrip() + "\"" + "\n" + \
                        "}")
                f.write(edit)
                f.close()
                runElGamal = "./ElGamal encryptToPubKey " + \
                    self.currentReceiver + ' ' + \
                    self.ElGamalKeyFileName + ' ' + \
                    "\'" + edit + "\' " + \
                    self.currentswapname + "/ENC_response_commitment.atomicswap"
                ElGamal = os.popen(runElGamal).read()
                f = open(self.currentswapname + "/ENC_response_commitment.atomicswap", "r")
                enc_response = f.read()
                f.close()
                pyperclip.copy(enc_response) #if the response wont paste into GUI entry encryption is too large
                self.swap_tab_view.checkButton.configure(state="normal")
                self.swap_tab_view.checkLockTimeButton.configure(state="normal")
    else:
        print("swap contract not deployed yet!")

def deployAndFundScalarSwapContract(self): #responder operation
    updateDataBasedOnOpenTab(self)
    if self.swap_tab_view.valueToSpendEntry.get() != "":
        AtomicityScalarContractOperation(self)
        customgas = False
        if self.swap_tab_view.GasEntry.get() != "":
            gas = self.swap_tab_view.GasEntry.get()
            customgas = True
        else:
            gas = "6000000"
        if self.swap_tab_view.GasModEntry.get() != "":
            gasMod = self.swap_tab_view.GasModEntry.get()
            customgas = True
        else:
            gasMod = "1"
        if customgas == False:
            addr = os.popen("cd Atomicity/" + self.currentswapname + "/ && python3 py/deploy.py").read()
            if addr.startswith("0x"):
                addrfile = open(self.currentswapname + "/responderContractAddress", "w")
                addrfile.write(addr)
                addrfile.close()
                #TODO: IMPORTANT! check the contract by comparing its x and y coordinates to make sure they are the ones expected
                #but more importantly to make sure the contract was properly uploaded to the chain before sending funds to it!!!
                fundScalarContract(self)
                self.swap_tab_view.copyResponseButton.configure(state="normal")
            else:
                print("addr should be output instead got:", addr)
        elif customgas == True:
            deployCMD = "cd Atomicity/" + self.currentswapname + "/ && python3 py/deploy.py deployCustomGas " + gas + " " + gasMod
            print(deployCMD)
            addr = os.popen(deployCMD).read()
            if addr.startswith("0x"):
                addrfile = open(self.currentswapname + "/responderContractAddress", "w")
                addrfile.write(addr)
                addrfile.close()
                #TODO: IMPORTANT! check the contract by comparing its x and y coordinates to make sure they are the ones expected
                #but more importantly to make sure the contract was properly uploaded to the chain before sending funds to it!!!
                fundScalarContract(self)
                self.swap_tab_view.copyResponseButton.configure(state="normal")
            else:
                print("addr should be output instead got:", addr)
    else:
        print("enter value to spend to contract before deploying (to prevent manual overspending)")

def fundScalarContract(self): #responder operation
    if os.path.isfile(self.currentswapname + "/responderContractAddress"):
        addr = open(self.currentswapname + "/responderContractAddress", "r").read().rstrip()
        cmd = "cd Atomicity/" + \
                self.currentswapname + " && ./deploy.sh sendAmount " + \
                self.swap_tab_view.valueToSpendEntry.get()  + ' '+ addr
        print(cmd)
        print(os.popen(cmd).read())
    else:
        print("responders contract not found! not deployed yet or recieved")

def writeInitiation(self): #responder operation
    f = open(self.currentswapname + "/initiation.atomicswap", "w")
    f.write(self.initiatorCommitment.get())
    f.close()

def decryptInitiation(self): #responder operation
    decryptElGamal = \
            "./ElGamal decryptFromPubKey " + self.currentswapname + "/initiation.atomicswap " + \
            self.currentReceiver + ' ' + self.ElGamalKeyFileName
    decryption = os.popen(decryptElGamal).read()
    f = open(self.currentswapname + "/DEC_initiation.atomicswap", "w")
    f.write(decryption)
    f.close()
    j = json.loads(decryption)
    self.counterpartyChainPubkey = j["chainPubkey"]
    self.ksG = j["ksG"]
    self.crossChain = j["localChain"] #When responder sending chainpubkey to counterparty, get key from this chain

def commitResponse(self): #responder operation 
    self.response = \
        os.popen(\
                "python3 -u SigmaParticle/AtomicMultiSigECC/py/deploy.py p2Respond " +\
                "'" + self.ksG + "' " + "'" + str(datetime.now()) + "' " +\
                self.currentswapname + "/sr " + self.currentswapname + "/x" \
                ).read()
    f = open(self.currentswapname + "/response_commitment.atomicswap", "w")
    f.write(self.response)
    f.close()
    j = json.loads(self.response)
    self.xG = j["xG"]
    runElGamal = "./ElGamal encryptToPubKey " + \
        self.currentReceiver + ' ' + \
        self.ElGamalKeyFileName + ' ' + \
        "\'" + self.response + "\' " + \
        self.currentswapname + "/ENC_response_commitment.atomicswap "
    self.encryption = os.popen(runElGamal).read()

def AtomicityScalarContractOperation(self): #responder operation 
    DURATION = "25"
    if self.swap_tab_view.CustomLockTimeEntry.get() != "":
        DURATION = self.swap_tab_view.CustomLockTimeEntry.get()
    cmd = "cd Atomicity && ./new_frame " + self.currentswapname  + \
        " -M -CA 4 " + "\\\"" + self.counterpartyChainPubkey + "\\\" " + \
        str(ast.literal_eval(self.xG)[0])  + " " + str(ast.literal_eval(self.xG)[1]) + " " + DURATION
    new_frame = os.popen(cmd)
    time.sleep(1) #wait for file to be built

    #copy in generic ECC timelock multisig contract for atomic swap
    os.remove("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol")
    contract_copy = \
            "cd Atomicity/" + self.currentswapname + "/contracts " + \
            "&& cp ../../AtomicMultiSigSecp256k1/contracts/AtomicMultiSigSecp256k1.sol " + self.currentswapname + ".sol" + \
            "&& cp ../../AtomicMultiSigSecp256k1/contracts/ReentrancyGuard.sol . " + \
            "&& cp ../../AtomicMultiSigSecp256k1/contracts/EllipticCurve.sol . "
    cpy = os.popen(contract_copy).read()
    rename = str(open("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol", "r").read() )
    rewrite = open("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol", "w")
    rewrite.write(rename.replace('AtomicMultiSigSecp256k1', self.currentswapname))
    rewrite.close()
    specifyChain = os.popen("echo 'CurrentChain=\"" + self.responderChainOption.get() + "\"' >> Atomicity/" + \
            self.currentswapname + "/.env").read()

def initiateSwap(self): #currently ambiguous as it facilitates initiator and responder swap start
    if self.isInitiator == True and (self.initiatorChain  == "NotSelected" or self.responderChain == "NotSelected"):
        print("at least one chain not selected! initiator must select both chains")
    elif self.isInitiator == False and self.responderChainOption  == "NotSelected":
        print("select the chain you are on!")
    elif self.initiatorChainOption == self.responderChain:
        print("same chain selected for both sides of swap!")
    else:
        self.currentReceiver = self.CounterpartyElGamalKey.get()
        if self.currentReceiver == "":
            print("receiver ElGamal Key not specified!")
        #elif len(self.currentReceiver) < 616:
        #    print("receiver ElGamal Key is less than 2048 bit")
        elif len(self.currentReceiver) < 405:
            print("receiver ElGamal Key is less than 1346 bit")
        elif any(c.isalpha() for c in self.currentReceiver):
            print("detected alphabetical characters, hexadecimal keys not implemented yet")
        elif self.isInitiator == True:
            initiatorStart(self)
            saveRole(self)
        elif self.isInitiator == False:
            #make sure active tab functions get swap name from current open tab
            self.currentswapname = determineSwapName()
            if self.swapTabSet == False:
                setSwapTab(self, True)
            else:
                setSwapTab(self, False)
            if self.initiatorCommitment.get() != "":
                writeInitiation(self)
                decryptInitiation(self)
                setCrossChainPubkeyDerived(self)
                GUI_ReArrange_Chain_Based(self)
                commitResponse(self)
                SwapResponderGUI(self)
                saveRole(self)
            else:
                print("paste in the encrypted initiator commitment")


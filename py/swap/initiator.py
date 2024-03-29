from datetime import datetime
import ast
import subprocess
from GUI_manager import *
from chain import setLocalChainPubkeyManual, setCrossChainPubkeyManual, setCrossChainPubkeyDerived
import tkinter, customtkinter, os, json, time, subprocess, sys, io, pyperclip
from tools import *
from file_tools import *

def initiatorStart(self, relevantTab): #initiator operation #start operations should not have update  functions at the beginning
                            #because they imply newly generated content
                            #update functions imply already generated content
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
            relevantTab + "/ENC_initiation.atomicswap "
    encryption = os.popen(runElGamal).read()
    clean_file_open(relevantTab + "/PRIV_initiation.atomicswap", "w", initiation)
    clean_file_open(relevantTab + "/initiation.atomicswap", "w", strippedInitiation6)
    clean_file_open(relevantTab + "/Receiver.ElGamalPub", "w", self.currentReceiver)
    clean_file_open(relevantTab + "/SenderKey.ElGamalPub", "w", self.ElGamalPublicKey)
    #maybe we can just backup the whole private keyfile in this instance
    if self.swapTabSet == False:
        setSwapTab(self, True)
    else:
        setSwapTab(self, False)


def copyENCInit(self, relevantTab):
    pyperclip.copy(clean_file_open(relevantTab + "/ENC_initiation.atomicswap", "r"))
    self.swap_tab_view.decryptResponderCommitmentButton.configure(state="normal")

    #make sure active tab functions get swap name from current open tab

def inspectScalarLockContract(self, relevantTab): #initiator operation
    decryptResponse(self, relevantTab)
    j = json.loads(clean_file_open(relevantTab + "/DEC_response.atomicswap", "r"))
    chain = j["chain"]
    contractAddr = j["contractAddr"]
    if chain == "Goerli":
        self.scalarContractFundingAmount = os.popen("cd Atomicity/Goerli && python3 -u py/deploy.py " + contractAddr).read()
    elif chain == "Sepolia":
        self.scalarContractFundingAmount = os.popen("cd Atomicity/Sepolia && python3 -u py/deploy.py getBalance " + contractAddr).read()
    self.swap_tab_view.responderContractValueLabel.configure(text= "Responder Contract Value: " +\
            self.scalarContractFundingAmount + " wei")
    if self.scalarContractFundingAmount.isdigit() == False:
        print("self.scalarContractFundingAmount is not digit, instead is :", self.scalarContractFundingAmount)
        return
    if int(self.scalarContractFundingAmount) > 0:
        self.swap_tab_view.finalizeSwapButton.configure(state="normal")
    print(self.scalarContractFundingAmount)



def decryptResponse(self, relevantTab): #initiator operation
    if os.path.isfile(relevantTab + "/response.atomicswap"):
        print("response commitment already collected for ", relevantTab)
    else:
        if self.swap_tab_view.responderCommitment.get() != "":
            clean_file_open(relevantTab + "/response.atomicswap", "w", self.swap_tab_view.responderCommitment.get())
            decryptElGamal = \
                        "./ElGamal decryptFromPubKey " + relevantTab + "/response.atomicswap " + \
                        self.currentReceiver + ' ' + self.ElGamalKeyFileName
            decrypt = os.popen(decryptElGamal).read()
            time.sleep(10)
            clean_file_open(relevantTab + "/DEC_response.atomicswap", "w", decrypt, "FAILED TO WRITE DECRYPTED RESPONSE FILE")
            print(decrypt)
        else:
            print("enter the commitment from responder!")


def draftFinalSignature(self, relevantTab): #create the final sig ss and pub value sG #initiator operation
    if os.path.isfile(relevantTab + "/finalize.atomicswap") == False or os.path.isfile("SigmaParticle/" + self.currentswapname + "/boxId") == False:
        updateDataBasedOnOpenTab(self)
        if int(self.swap_tab_view.initiatorContractValueEntry.get()) >= 123841:
            j = json.loads(clean_file_open(relevantTab + "/DEC_response.atomicswap", "r"))
            sr_ = j["sr_"]
            xG = j["xG"]
            srG = j["srG"]
            e = j["e"]
            j = json.loads(clean_file_open(relevantTab + "/PRIV_initiation.atomicswap", "r"))
            ks = j["ks"]
            rs = j["rs"]
            cmd = "cd SigmaParticle/AtomicMultiSigECC/ && python3 -u py/deploy.py p1Finalize " + \
                    "\"" + str(sr_) + "\"" + " \"" + xG.replace(" ", "") + "\" \"" + srG.replace(" ", "") + "\" \"" + str(e) + "\" " + \
                    "\"" + str(ks) + "\"" + " \"" + str(rs) + "\""
            finalSigJson = os.popen(cmd).read()
            if json.loads(finalSigJson) != ValueError and finalSigJson != "":
                print(finalSigJson)
                clean_file_open(relevantTab + "/finalize.atomicswap", "w", finalSigJson)
                SigmaParticleAtomicSchnorr(self, relevantTab)
                time.sleep(10)
                boxId = clean_file_open("SigmaParticle/" + relevantTab + "/boxId", "r")
                mod = finalSigJson
                modified = mod.replace("\"\n}", "\",\n    \"boxId\": \"" + str(boxId) + "\"\n}")
                print(modified)
                clean_file_open(relevantTab + "/finalize.atomicswap", "w", modified)
                cmd = \
                    "./ElGamal encryptToPubKey " + \
                    self.currentReceiver + ' ' + \
                    self.ElGamalKeyFileName + ' ' + \
                    "\'" + modified + "\' " + \
                    relevantTab + "/ENC_finalize.atomicswap"
                encrypt = os.popen(cmd).read()
                encryption = clean_file_open(relevantTab + "/ENC_finalize.atomicswap", "r")
                #now upload ergoscript contract
                pyperclip.copy(encryption)
                self.swap_tab_view.finalizeCheck.configure(state="normal")
        else:
            print("you must spend minimum 123841 nanoErg into the contract or else it is unclaimable!")


    if os.path.isfile("SigmaParticle/" + relevantTab + "/boxId") == True: #if we already have the box we have properly uploaded the contract
        encryption = clean_file_open(relevantTab + "/ENC_finalize.atomicswap", "r")
        pyperclip.copy(encryption)

def checkTreeForFinalization(self, relevantTab):
    tree = clean_file_open("SigmaParticle/" + relevantTab + "/ergoTree", "r")
    if clean_file_open(relevantTab + "/finalize.atomicswap", "r") == None:
        return print("finalization not created yet...")
    else:
        j = json.loads(clean_file_open(relevantTab + "/finalize.atomicswap", "r"))
        if "boxId" in j.keys():
            boxId = j["boxId"]
            treeToAddrCmd = \
                    "cd SigmaParticle/treeToAddr && ./deploy.sh " + tree
            addr = json.loads(os.popen(treeToAddrCmd).read())["address"]
            print("addr: ", addr)
            boxFilterCmd =\
                    "cd SigmaParticle/boxFilter &&" +\
                    "./deploy.sh " + addr + " " + boxId + " ../../" + relevantTab + "/atomicClaim"
            print(os.popen(boxFilterCmd).read())
            if os.path.isfile(relevantTab + "/atomicClaim_tx1"):
                j = json.loads(clean_file_open(relevantTab + "/atomicClaim_tx1", "r"))
                R4 = j["outputs"][0]["additionalRegisters"]["R4"]
                clean_file_open(relevantTab + "/sr", "w", R4)
                self.swap_tab_view.claim.configure(state="normal")
            else:
                print("no atomic claim transactions found")
        else:
            print("boxID not created yet")


def deduce_x(self, relevantTab):

    j = json.loads(clean_file_open(relevantTab + "/DEC_response.atomicswap", "r"))
    sr_ = j["sr_"]
    contractAddr = j["contractAddr"]
    chain = j["chain"]
    sr = clean_file_open(relevantTab + "/sr", "r")
    decodeCMD = \
            "cd SigmaParticle/valFromHex && ./deploy.sh " + sr + " ../../" + relevantTab + "/decoded_sr"
    decodeResponse = os.popen(decodeCMD).read()
    dec_sr = clean_file_open(relevantTab + "/decoded_sr", "r")
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
    return os.popen(claimScript).read()

def deploySigmaParticleAtomicSchorr(self, relevantTab):
    command = "cd SigmaParticle/" + relevantTab + " && ./deploy.sh deposit"
    devnull = open(os.devnull, 'wb')
    response = subprocess.Popen(command, shell=True,
                         stdout=devnull, stderr=devnull,
                         close_fds=True)

def SigmaParticleRefund(self, relevantTab):
    devnull = open(os.devnull, 'wb')
    boxId = clean_file_open("SigmaParticle/" + relevantTab + "/boxId", "r")
    echoBoxIdCMD = \
            "echo '\natomicBox=" + boxId + "' >> SigmaParticle/" + relevantTab + "/.env"
    os.popen(echoBoxIdCMD).read()

    cmd =  "cd SigmaParticle/" + relevantTab + "&& ./deploy.sh refund"
    return os.popen(cmd).read()


def SigmaParticleAtomicSchnorr(self, relevantTab):
    response = clean_file_open(relevantTab + "/DEC_response.atomicswap", "r")
    j = json.loads(response)
    krG = ast.literal_eval(j["krG"])
    srG = ast.literal_eval(j["srG"])
    finalize = clean_file_open(relevantTab + "/finalize.atomicswap", "r")
    j = json.loads(finalize)
    ssG = ast.literal_eval(j["ssG"])
    j = json.loads(clean_file_open(relevantTab + "/initiation.atomicswap", "r"))
    ksG = ast.literal_eval(j["ksG"])
    j = json.loads(clean_file_open(relevantTab + "/DEC_response.atomicswap", "r"))
    receiver = j[self.initiatorChain + "_chainPubkey"]
    if self.swap_tab_view.refundDurationEntry.get() == "":
        refundDuration = 25
    else:
        refundDuration = self.swap_tab_view.refundDurationEntry.get()
    cmd = "cd SigmaParticle && ./new_frame " + str(relevantTab) + \
            " && cd " + str(relevantTab) + " && echo " + \
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
    copyScriptsCommand = "cp SigmaParticle/AtomicMultiSig/py/main.py SigmaParticle/" + relevantTab + "/py/main.py"
    copyScripts = os.popen(copyScriptsCommand).read()
    deploySigmaParticleAtomicSchorr(self , relevantTab)
    self.swap_tab_view.checkRefundLockTime.configure(state="normal")


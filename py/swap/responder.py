from datetime import datetime
import ast
from tools import *
from GUI_manager import *
from chain import setLocalChainPubkeyManual, setCrossChainPubkeyManual, setCrossChainPubkeyDerived
import tkinter, customtkinter, os, json, time, subprocess, sys, io, pyperclip

def responderClaim(self, relevantTab):
    updateDataBasedOnOpenTab(self)
    if os.path.isfile(relevantTab + "/ENC_Finalization.atomicswap") == False:
        print("finalization not found! paste in finalization and check contract value first!")
    else:
        newContractCmd = "cd SigmaParticle && ./new_frame " + relevantTab
        print(os.popen(newContractCmd).read())
        copyBoilerplateCmd = "cp SigmaParticle/AtomicMultiSig/py/main.py SigmaParticle/" + relevantTab  + "/py/main.py"
        print(os.popen(copyBoilerplateCmd).read())
        sr = clean_file_open(relevantTab + "/sr", "r")
        j = json.loads(clean_file_open(relevantTab + "/DEC_Finalization.atomicswap", "r"))
        ss = j["ss"]
        ksG = json.loads(clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "r"))["ksG"]
        krG = json.loads(clean_file_open(relevantTab + "/response_commitment.atomicswap", "r"))["krG"]
        j = json.loads(clean_file_open(relevantTab + "/DEC_Finalization.atomicswap", "r"))
        boxId = j["boxId"]
        nanoErgs = clean_file_open(relevantTab + "/InitiatorContractValue", "r")
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
                "\" >> SigmaParticle/" + relevantTab + "/.env"
        print(os.popen(echoVariablesCMD).read())
        claimCMD = \
                "cd SigmaParticle/" + relevantTab + " && ./deploy.sh claim"
        returnVal = os.popen(claimCMD).read()
        time.sleep(5)
        return returnVal


def responderCheck(self, relevantTab): #responder operatio
    updateDataBasedOnOpenTab(self)
    if self.swap_tab_view.finalizeEntry.get() == "":
        print("paste in the finalization to claim!")
    else:
        ENCFin = self.swap_tab_view.finalizeEntry.get()
        clean_file_open(relevantTab + "/ENC_Finalization.atomicswap", "w", ENCFin)
        decryptElGamal = \
            "./ElGamal decryptFromPubKey " + relevantTab + "/ENC_Finalization.atomicswap " + \
            self.currentReceiver + ' ' + self.ElGamalKeyFileName
        decryption = os.popen(decryptElGamal).read()
        clean_file_open(relevantTab + "/DEC_Finalization.atomicswap", "w", decryption)
        j = json.loads(decryption)
        boxValCheck = "cd SigmaParticle/boxValue && ./deploy.sh " +\
                j["boxId"] + " ../../" +\
                relevantTab + "/InitiatorContractValue"
        devnull = open(os.devnull, 'wb')
        p = subprocess.Popen(boxValCheck, shell=True,
                         stdout=devnull, stderr=devnull,
                         close_fds=True)
        if os.path.isfile(relevantTab + "/InitiatorContractValue") == True:
            nanoErgs = clean_file_open(relevantTab + "/InitiatorContractValue", "r")
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

def AtomicityRefund(self, relevantTab):
    updateDataBasedOnOpenTab(self)
    addr = json.loads(clean_file_open(relevantTab + "/response_commitment.atomicswap", "r"))["contractAddr"]
    refundCMD = \
            "cd Atomicity/" + relevantTab + " && ./deploy.sh refund " + addr
    return os.popen(refundCMD).read()

def copyResponse(self, relevantTab): #esponder operation
    updateDataBasedOnOpenTab(self)
    if os.path.isfile(relevantTab + "/ENC_response_commitment.atomicswap"):
        enc_response = clean_file_open(relevantTab + "/ENC_response_commitment.atomicswap", "r")
        pyperclip.copy(enc_response) #if the response wont paste into GUI entry encryption is too large
        self.swap_tab_view.checkButton.configure(state="normal")
        self.swap_tab_view.checkLockTimeButton.configure(state="normal")
    else:
        print("cannot find: " + relevantTab + "/ENC_response_commitment.atomicswap")

def deployAndFundScalarSwapContract(self, relevantTab): #responder operation
    updateDataBasedOnOpenTab(self)
    if self.swap_tab_view.valueToSpendEntry.get() != "":
        AtomicityScalarContractOperation(self, relevantTab)
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
            addr = os.popen("cd Atomicity/" + relevantTab + "/ && python3 py/deploy.py").read()
            if addr.startswith("0x"):
                clean_file_open(relevantTab + "/responderContractAddress", "w", addr)
                #TODO: IMPORTANT! check the contract by comparing its x and y coordinates to make sure they are the ones expected
                #but more importantly to make sure the contract was properly uploaded to the chain before sending funds to it!!!
                fundScalarContract(self, relevantTab)
                self.swap_tab_view.copyResponseButton.configure(state="normal")
                if os.path.isfile(relevantTab + "/responderContractAddress"):
                    if os.path.isfile(self.swap_tab_view.get() + "/response_commitment.atomicswap"):
                        addr = clean_file_open(relevantTab + "/responderContractAddress", "r").rstrip()
                        response = clean_file_open(self.swap_tab_view.get() + "/response_commitment.atomicswap", "r")
                        if "chain" not in response :
                            j = json.loads(clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "r"))
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
                            clean_file_open(self.swap_tab_view.get() + "/response_commitment.atomicswap", \
                                    "w", edit, "failed to update response committment")
                            runElGamal = "./ElGamal encryptToPubKey " + \
                                self.currentReceiver + ' ' + \
                                self.ElGamalKeyFileName + ' ' + \
                                "\'" + edit + "\' " + \
                                relevantTab + "/ENC_response_commitment.atomicswap"
                            ElGamal = os.popen(runElGamal).read()
            else:
                print("addr should be output instead got:", addr)
        elif customgas == True:
            deployCMD = "cd Atomicity/" + relevantTab + "/ && python3 py/deploy.py deployCustomGas " + gas + " " + gasMod
            print(deployCMD)
            addr = os.popen(deployCMD).read()
            if addr.startswith("0x"):
                clean_file_open(relevantTab + "/responderContractAddress", "w", addr)
                #TODO: IMPORTANT! check the contract by comparing its x and y coordinates to make sure they are the ones expected
                #but more importantly to make sure the contract was properly uploaded to the chain before sending funds to it!!!
                fundScalarContract(self, relevantTab)
                self.swap_tab_view.copyResponseButton.configure(state="normal")
                if os.path.isfile(relevantTab + "/responderContractAddress"):
                    if os.path.isfile(self.swap_tab_view.get() + "/response_commitment.atomicswap"):
                        addr = clean_file_open(relevantTab + "/responderContractAddress", "r").rstrip()
                        response = clean_file_open(self.swap_tab_view.get() + "/response_commitment.atomicswap", "r")
                        if "chain" not in response :
                            j = json.loads(clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "r"))
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
                            clean_file_open(self.swap_tab_view.get() + "/response_commitment.atomicswap", \
                                    "w", edit, "failed to update response committment")
                            runElGamal = "./ElGamal encryptToPubKey " + \
                                self.currentReceiver + ' ' + \
                                self.ElGamalKeyFileName + ' ' + \
                                "\'" + edit + "\' " + \
                                relevantTab + "/ENC_response_commitment.atomicswap"
                            ElGamal = os.popen(runElGamal).read()
            else:
                print("addr should be output instead got:", addr)
        verify = "cd Atomicity/" + relevantTab + "/ && python3 py/deploy.py verify"
        os.popen(verify).read()
    else:
        print("enter value to spend to contract before deploying (to prevent manual overspending)")

def fundScalarContract(self, relevantTab): #responder operation
    if os.path.isfile(relevantTab + "/responderContractAddress"):
        addr = clean_file_open(relevantTab + "/responderContractAddress", "r").rstrip()
        cmd = "cd Atomicity/" + \
                relevantTab + " && ./deploy.sh sendAmount " + \
                self.swap_tab_view.valueToSpendEntry.get()  + ' '+ addr
        print(cmd)
        print(os.popen(cmd).read())
    else:
        print("responders contract not found! not deployed yet or recieved")

def writeInitiation(self, relevantTab): #responder operation
    clean_file_open(relevantTab + "/initiation.atomicswap", "w", self.initiatorCommitment.get())

def decryptInitiation(self, relevantTab): #responder operation
    decryptElGamal = \
            "./ElGamal decryptFromPubKey " + relevantTab + "/initiation.atomicswap " + \
            self.currentReceiver + ' ' + self.ElGamalKeyFileName
    decryption = os.popen(decryptElGamal).read()
    clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "w", decryption)
    j = json.loads(decryption)
    self.counterpartyChainPubkey = j["chainPubkey"]
    self.ksG = j["ksG"]
    self.crossChain = j["localChain"] #When responder sending chainpubkey to counterparty, get key from this chain

def commitResponse(self, relevantTab): #responder operation
    self.response = \
        os.popen(\
                "python3 -u SigmaParticle/AtomicMultiSigECC/py/deploy.py p2Respond " +\
                "'" + self.ksG + "' " + "'" + str(datetime.now()) + "' " +\
                relevantTab + "/sr " + self.currentswapname + "/x" \
                ).read()
    clean_file_open(relevantTab + "/response_commitment.atomicswap", "w", self.response)
    j = json.loads(self.response)
    self.xG = j["xG"]
    runElGamal = "./ElGamal encryptToPubKey " + \
        self.currentReceiver + ' ' + \
        self.ElGamalKeyFileName + ' ' + \
        "\'" + self.response + "\' " + \
        relevantTab + "/ENC_response_commitment.atomicswap "
    self.encryption = os.popen(runElGamal).read()


def AtomicityScalarContractOperation(self, relevantTab): #responder operation
    DURATION = "200"
    if self.swap_tab_view.CustomLockTimeEntry.get() != "":
        DURATION = self.swap_tab_view.CustomLockTimeEntry.get()
    cmd = "cd Atomicity && ./new_frame " + relevantTab  + \
        " -M -CA 4 " + "\\\"" + self.counterpartyChainPubkey + "\\\" " + \
        str(ast.literal_eval(self.xG)[0])  + " " + str(ast.literal_eval(self.xG)[1]) + " " + DURATION
    new_frame = os.popen(cmd)
    time.sleep(1) #wait for file to be built

    #copy in generic ECC timelock multisig contract for atomic swap
    os.remove("Atomicity/" + relevantTab + "/contracts/" + self.currentswapname + ".sol")
    contract_copy = \
            "cd Atomicity/" + relevantTab + "/contracts " + \
            "&& cp ../../AtomicMultiSigSecp256k1/contracts/AtomicMultiSigSecp256k1.sol " + relevantTab + ".sol" + \
            "&& cp ../../AtomicMultiSigSecp256k1/contracts/ReentrancyGuard.sol . " + \
            "&& cp ../../AtomicMultiSigSecp256k1/contracts/EllipticCurve.sol . "
    cpy = os.popen(contract_copy).read()
    rename = str(clean_file_open("Atomicity/" + relevantTab + "/contracts/" + self.currentswapname + ".sol", "r"))
    clean_file_open("Atomicity/" + relevantTab + "/contracts/" + self.currentswapname + ".sol", "w", \
            rename.replace('AtomicMultiSigSecp256k1', relevantTab))
    specifyChain = os.popen("echo 'CurrentChain=\"" + self.responderChainOption.get() + "\"' >> Atomicity/" + \
            relevantTab + "/.env").read()


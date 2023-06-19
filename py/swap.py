from datetime import datetime
import ast
import subprocess
import sys
sys.path.append('py/swap')
from initiator import *
from chain import setLocalChainPubkeyManual, setCrossChainPubkeyManual, setCrossChainPubkeyDerived
import tkinter, customtkinter, os, json, time, subprocess, io, pyperclip

class SwapTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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

def AtomicityRefund(self):
    updateDataBasedOnOpenTab(self)
    f = open(self.currentswapname + "/response_commitment.atomicswap", "r")
    addr = json.loads(f.read())["contractAddr"]
    f.close()
    
    refundCMD = \
            "cd Atomicity/" + self.currentswapname + " && ./deploy.sh refund " + addr
    print(os.popen(refundCMD).read())

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
    print(os.popen(cmd).read())



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
    DURATION = "200"
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


from datetime import datetime
import ast
import subprocess
import sys
sys.path.append('py/swap')
from initiator import *
from responder import *
from chain import setLocalChainPubkeyManual, setCrossChainPubkeyManual, setCrossChainPubkeyDerived
import tkinter, customtkinter, os, json, time, subprocess, io, pyperclip
import file_tools
class SwapTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

def nanoErgToErgo(nanoErgs): #only for round amounts
    return int(int(nanoErgs) / 1000000000)

def AutoClaim(self, relevantTab):
    while True:
        if os.path.isfile(relevantTab + "/AutoClaim"):
            b = clean_file_open(relevantTab + "/AutoClaim", "r")
            if  b == "false":
                print("autoclaim set to false: stopping")
                break
            else:
                if os.path.isfile(relevantTab + "/roleData.json") == True:
                    role = json.loads(clean_file_open(relevantTab + "/roleData.json", "r"))["role"]
                    if role == "responder":
                        if os.path.isfile(relevantTab + "/DEC_initiation.atomicswap") == True:
                            j = json.loads(clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "r"))
                            if j["localChain"] == "Ergo": #user is responding to initiator, who's `localChain` is Ergo
                                if os.path.isfile(relevantTab + "/InitiatorContractValue"):
                                    val = clean_file_open(relevantTab + "/InitiatorContractValue", "r")
                                    minimum = self.swap_tab_view.minimumValueAutoClaim.get()
                                    if minimum == "":
                                        print("enter minimum val!")
                                        clean_file_open(relevantTab + "/AutoClaim", "w", "false", truncate=True)
                                        self.swap_tab_view.tab(relevantTab).children["!ctkcheckbox"].toggle()
                                        break
                                    else:
                                        if int(minimum) < int(val):
                                            return responderClaim(self, relevantTab)
                                            break
                                        else:
                                            print("under minimum value")
                    if role == "initiator":
                        localChain = json.loads(clean_file_open(relevantTab +"/initiation.atomicswap", "r"))["localChain"]
                        if localChain == "Ergo":
                            if os.path.isfile(relevantTab + "/atomicClaim_tx1") and os.path.isfile(relevantTab + "/sr"):
                                try:
                                    if os.path.isfile(relevantTab + "/DEC_response.atomicswap") == True:
                                        j = json.loads(clean_file_open(relevantTab + "/DEC_response.atomicswap", "r"))
                                        if j["chain"] == "Sepolia": #responder is on sepolia chain
                                            print("autoclaiming!")
                                            return deduce_x(self, relevantTab)
                                            break
                                except:
#                                    print("failure: retrying in five...")
#                                    time.sleep(5)
                                    break
                            else:
                                print("atomicClaim file not found, rechecking tree...")
                                t = threading.Thread(target=checkTreeForFinalization, args=(self, relevantTab))
                                t.start()
                                time.sleep(5)
                                break
                else:
                    break
        else:
            print("cant find path: " +  relevantTab + "/AutoClaim")

def AutoRefund(self, relevantTab):
    if os.path.isfile(relevantTab + "/roleData.json") == True:
        role = json.loads(clean_file_open(relevantTab + "/roleData.json", "r"))["role"]
        if role == "responder":
            print("role is responder...")
            if os.path.isfile(relevantTab + "/response_commitment.atomicswap"):
                j = json.loads(clean_file_open(relevantTab + "/response_commitment.atomicswap", "r"))
                if "chain" in j:
                    chain = j["chain"]
                    if chain == "Sepolia":
                        print("chain is Sepolia")
                        lockTime = getLocalLockTime(self, relevantTab)
                        print("lockTime = ", lockTime)
                        if lockTime != "":
                            if type(lockTime) != type(None):
                                if int(lockTime) <= 0 or int(lockTime) == 0:  
                                    response = AtomicityRefund(self, relevantTab)
                                    print("refundResponse: \n", response)
                                    if "Traceback" not in response:
                                        return "Success"
                                    else:
                                        return "Fail"
        if role == "initiator": #TODO
            print("role is initiator...")
            localChain = json.loads(clean_file_open(relevantTab +"/initiation.atomicswap", "r"))["localChain"]
            if localChain == "Ergo":
                print("chain is Ergo")
                if os.path.isfile("SigmaParticle/" + relevantTab + "/boxId"):
                    lockTime = getLocalLockTime(self, relevantTab)
                    print("lockTime = ", lockTime)
                    if lockTime != "":
                        if type(lockTime) != type(None):
                            if int(lockTime) <= 0 or int(lockTime) == 0:
                                response = SigmaParticleRefund(self, relevantTab)
                                print("refundResponse: \n", response)
                                if "error" not in response:
                                    return "Success"
                                else:
                                    return "Fail"
                else:
                    print("boxID not created yet")


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
            self.currentswapname = determineSwapName()
            initiatorStart(self, self.currentswapname)
            saveRole(self)
        elif self.isInitiator == False:
            #make sure active tab functions get swap name from current open tab
            self.currentswapname = determineSwapName()
            relevantTab = self.currentswapname
            if self.initiatorCommitment.get() != "":
                writeInitiation(self, relevantTab)
                decryptInitiation(self, relevantTab)
                setCrossChainPubkeyDerived(self)
                GUI_ReArrange_Chain_Based(self)
                commitResponse(self, relevantTab)
#                SwapResponderGUI(self)
                saveRole(self)
            else:
                print("paste in the encrypted initiator commitment")
            if self.swapTabSet == False:
                setSwapTab(self, True)
            else:
                setSwapTab(self, False, relevantTab)


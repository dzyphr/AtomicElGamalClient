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
                                        self.swap_tab_view.autoClaimCheckbox.toggle()
                                        break
                                    else:
                                        if int(minimum) < int(val):
                                            return responderClaim(self, relevantTab)
                                            break
                                        else:
                                            print("under minimum value")
                else:
                    time.sleep(5)
        else:
            print("cant find path: " +  relevantTab + "/AutoClaim")



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
            relevantTab = self.currentswapname
            if self.swapTabSet == False:
                setSwapTab(self, True)
            else:
                setSwapTab(self, False)
            if self.initiatorCommitment.get() != "":
                writeInitiation(self, relevantTab)
                decryptInitiation(self, relevantTab)
                setCrossChainPubkeyDerived(self)
                GUI_ReArrange_Chain_Based(self)
                commitResponse(self, relevantTab)
                SwapResponderGUI(self)
                saveRole(self)
            else:
                print("paste in the encrypted initiator commitment")


import tkinter, customtkinter, os, json, time
from GUI_manager import *
chains = ["NotSelected", "Ergo", "Goerli", "Sepolia"]

#TODO: The chainpubkey is based on the RECIEVERS CHAIN!!! not senders chain... need to create clear path for setting these things
#ex: p1 is on ergo, he ALSO needs a EVM keypair to complete the swap ! thus get his EVM key for this purpose
#send EVM pubkey if receiverChain is Goerli and isInitiator == True


def setInitiatorChain(self, choice):
    self.initiatorChain = choice
    print(self.initiatorChain)
    GUI_ReArrange_Chain_Based(self)

def setResponderChain(self, choice):
    self.responderChain = choice
    print(self.responderChain)
    GUI_ReArrange_Chain_Based(self)


def setLocalChainPubkeyManual(self):
    if self.isInitiator == False:
        if self.responderChain == "Ergo":
            self.chainPubkey = os.popen("python3 -u SwapKeyManager/py/deploy.py getPubkey " + self.chainPubkeyEntry.get()).read()
        elif self.responderChain == "Goerli":
            self.chainPubkey = os.popen("python3 Atomicity/Goerli/py/deploy.py getAccount").read()
        elif self.responderChain == "Sepolia":
            self.chainPubkey = os.popen("python3 Atomicity/Sepolia/py/deploy.py getAccount").read()
    elif self.isInitiator == True:
        if self.initiatorChain == "Ergo":
            self.chainPubkey = os.popen("python3 -u SwapKeyManager/py/deploy.py getPubkey " + self.chainPubkeyEntry.get()).read()
        elif self.initiatorChain == "Goerli":
            self.chainPubkey = os.popen("python3 Atomicity/Goerli/py/deploy.py getAccount").read()
        elif self.initiatorChain == "Sepolia":
            self.chainPubkey = os.popen("python3 Atomicity/Sepolia/py/deploy.py getAccount").read()

#TODO: merklize chainpubkey into local and cross chainpubkey vars
def setCrossChainPubkeyManual(self):
    if self.isInitiator == True:
        if self.responderChain == "Ergo":
            self.chainPubkey = os.popen("python3 -u SwapKeyManager/py/deploy.py getPubkey " + self.chainPubkeyEntry.get()).read()
        elif self.responderChain == "Goerli":
            self.chainPubkey = os.popen("python3 Atomicity/Goerli/py/deploy.py getAccount").read()
        elif self.responderChain == "Sepolia":
            self.chainPubkey = os.popen("python3 Atomicity/Sepolia/py/deploy.py getAccount").read()
    elif self.isInitiator == False:
        if self.initiatorChain == "Ergo":
            self.chainPubkey = os.popen("python3 -u SwapKeyManager/py/deploy.py getPubkey " + self.chainPubkeyEntry.get()).read()
        elif self.initiatorChain == "Goerli":
            self.chainPubkey = os.popen("python3 Atomicity/Goerli/py/deploy.py getAccount").read()
        elif self.initiatorChain == "Sepolia":
            self.chainPubkey = os.popen("python3 Atomicity/Sepolia/py/deploy.py getAccount").read()

def setCrossChainPubkeyDerived(self):
    if self.crossChain == "Ergo":
        if self.chainPubkeyEntry.get() == "":
            self.chainPubkeyEntry.insert(0, "0")
        self.chainPubkey = os.popen("python3 -u SwapKeyManager/py/deploy.py getPubkey " + self.chainPubkeyEntry.get()).read()
    elif self.crossChain == "Goerli":
        self.chainPubkey = os.popen("python3 Atomicity/Goerli/py/deploy.py getAccount").read()
    elif self.crossChain == "Sepolia":
        self.chainPubkey = os.popen("python3 Atomicity/Sepolia/py/deploy.py getAccount").read()


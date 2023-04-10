import tkinter, customtkinter, os, json, time
from GUI_manager import *
chains = ["NotSelected", "Ergo", "Goerli"]

#TODO: The chainpubkey is based on the RECIEVERS CHAIN!!! not senders chain... need to create clear path for setting these things
#ex: p1 is on ergo, he ALSO needs a EVM keypair to complete the swap ! thus get his EVM key for this purpose
#send EVM pubkey if receiverChain is Goerli and isInitiator == True


def setSenderChain(self, choice):
    self.senderChain = choice
    print(self.senderChain)
    GUI_ReArrange_Chain_Based(self)

def setReceiverChain(self, choice):
    self.receiverChain = choice
    print(self.receiverChain)
    GUI_ReArrange_Chain_Based(self)

def setChainPubkey(self):
    if self.receiverChain == "Ergo":
        self.chainPubkey = os.popen("python3 -u SwapKeyManager/py/deploy.py getPubkey " + self.chainPubkeyEntry.get()).read()
    if self.receiverChain == "Goerli":
        self.chainPubkey = os.popen("python3 Atomicity/basic_framework/py/deploy.py getAccount").read()


import tkinter, customtkinter, os, json, time
chains = ["NotSelected", "Ergo", "Goerli"]

#TODO: The chainpubkey is based on the RECIEVERS CHAIN!!! not senders chain... need to create clear path for setting these things
#ex: p1 is on ergo, he ALSO needs a EVM keypair to complete the swap ! thus get his EVM key for this purpose
#send EVM pubkey if receiverChain is Goerli and isInitiator == True


def GUI_ReArrange_Chain_Based(self):
    if self.senderChain == "Ergo" or self.receiverChain == "Ergo": #future make this all non account chains
        self.fromChainLabel.pack_forget()
        self.fromChain.pack_forget() #unpack
        self.toChainLabel.pack_forget()
        self.toChain.pack_forget()
        self.initiateButton.pack_forget()
        self.initiatorCheckbox.pack_forget()
        self.initiatorCommitLabel.pack_forget()
        self.initiatorCommitment.pack_forget()
        self.responseCommitLabel.pack_forget()
        self.respondButton.pack_forget()

        self.chainPubkeyLabel.pack(pady=2, padx=2)
        self.chainPubkeyEntry.pack(pady=2, padx=2) #introduce derived public key indexer for non account chains
        self.setChainPubkey.pack(pady=2, padx=2)

        self.fromChainLabel.pack(pady=2, padx=2)
        self.fromChain.pack(pady=2, padx=2) #repack
        self.toChainLabel.pack(pady=2, padx=2)
        self.toChain.pack(pady=2, padx=2)
        self.initiatorCheckbox.pack(pady=2, padx=2)
        self.initiateButton.pack(pady=2, padx=2)
        self.initiatorCheckbox.pack(pady=2, padx=2)
        from swap import GUI_Arrange_Swap_Based
        GUI_Arrange_Swap_Based(self)
    else:
        self.chainPubkeyLabel.pack_forget()
        self.chainPubkeyEntry.pack_forget()
        self.setChainPubkey.pack_forget()
        self.fromChainLabel.pack_forget()
        self.fromChain.pack_forget() #unpack
        self.toChainLabel.pack_forget()
        self.toChain.pack_forget()                  #remove indexer for account chains
        self.initiateButton.pack_forget()
        self.initiatorCheckbox.pack_forget()
        self.initiatorCommitLabel.pack_forget()
        self.initiatorCommitment.pack_forget()
        self.responseCommitLabel.pack_forget()
        self.respondButton.pack_forget()
        self.fromChainLabel.pack(pady=2, padx=2)
        self.fromChain.pack(pady=2, padx=2) #repack
        self.toChainLabel.pack(pady=2, padx=2)
        self.toChain.pack(pady=2, padx=2)
        self.initiatorCheckbox.pack(pady=2, padx=2)
        self.initiateButton.pack(pady=2, padx=2)
        self.initiatorCheckbox.pack(pady=2, padx=2)
        from swap import GUI_Arrange_Swap_Based
        GUI_Arrange_Swap_Based(self)



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


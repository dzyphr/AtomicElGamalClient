import tkinter, customtkinter, os, json, time

chains = ["NotSelected", "Ergo", "Goerli"]

def setSenderChain(self, choice):
    self.senderChain = choice
    print(self.senderChain)
    if self.senderChain == "Ergo": #TODO: make this for all non account model chains
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

        self.chainPubkeyLabel.pack(pady=12, padx=10)
        self.chainPubkeyEntry.pack(pady=12, padx=10)
        self.setChainPubkey.pack(pady=12, padx=10)

        self.fromChainLabel.pack()
        self.fromChain.pack() #repack
        self.toChainLabel.pack()
        self.toChain.pack()
        self.initiatorCheckbox.pack()
        self.initiateButton.pack()
        self.initiatorCheckbox.pack()
        if self.isInitiator == False:
            self.initiatorCommitLabel.pack()
            self.initiatorCommitment.pack()
            self.responseCommitLabel.pack()
            self.respondButton.pack()

    else:
        self.chainPubkeyLabel.pack_forget()
        self.chainPubkeyEntry.pack_forget()
        self.setChainPubkey.pack_forget()
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
        self.fromChainLabel.pack()
        self.fromChain.pack() #repack
        self.toChainLabel.pack()
        self.toChain.pack()
        self.initiatorCheckbox.pack()
        self.initiateButton.pack()
        self.initiatorCheckbox.pack()
        if self.isInitiator == False:
            self.initiatorCommitLabel.pack()
            self.initiatorCommitment.pack()
            self.responseCommitLabel.pack()
            self.respondButton.pack()

def setReceiverChain(self, choice):
    self.receiverChain = choice
    print(self.receiverChain)

def setChainPubkey(self):
    self.chainPubkey = os.popen("python3 -u SwapKeyManager/py/deploy.py getPubkey " + self.chainPubkeyEntry.get()).read()
    print(self.chainPubkey)


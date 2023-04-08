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

        self.chainPubkeyLabel.pack(pady=2, padx=2)
        self.chainPubkeyEntry.pack(pady=2, padx=2)
        self.setChainPubkey.pack(pady=2, padx=2)

        self.fromChainLabel.pack(pady=2, padx=2)
        self.fromChain.pack(pady=2, padx=2) #repack
        self.toChainLabel.pack(pady=2, padx=2)
        self.toChain.pack(pady=2, padx=2)
        self.initiatorCheckbox.pack(pady=2, padx=2)
        self.initiateButton.pack(pady=2, padx=2)
        self.initiatorCheckbox.pack(pady=2, padx=2)
        if self.isInitiator == False:
            self.initiatorCommitLabel.pack(pady=2, padx=2)
            self.initiatorCommitment.pack(pady=2, padx=2)
            self.responseCommitLabel.pack(pady=2, padx=2)
            self.respondButton.pack(pady=2, padx=2)

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
        self.fromChainLabel.pack(pady=2, padx=2)
        self.fromChain.pack(pady=2, padx=2) #repack
        self.toChainLabel.pack(pady=2, padx=2)
        self.toChain.pack(pady=2, padx=2)
        self.initiatorCheckbox.pack(pady=2, padx=2)
        self.initiateButton.pack(pady=2, padx=2)
        self.initiatorCheckbox.pack(pady=2, padx=2)
        if self.isInitiator == False:
            self.initiatorCommitLabel.pack(pady=2, padx=2)
            self.initiatorCommitment.pack(pady=2, padx=2)
            self.responseCommitLabel.pack(pady=2, padx=2)
            self.respondButton.pack(pady=2, padx=2)

def setReceiverChain(self, choice):
    self.receiverChain = choice
    print(self.receiverChain)

def setChainPubkey(self):
    self.chainPubkey = os.popen("python3 -u SwapKeyManager/py/deploy.py getPubkey " + self.chainPubkeyEntry.get()).read()
    print(self.chainPubkey)


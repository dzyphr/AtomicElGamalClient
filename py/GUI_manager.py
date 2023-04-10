#######MAIN#########
def unpackMainGUI(self):
    self.fromChainLabel.pack_forget()
    self.fromChain.pack_forget() 
    self.toChainLabel.pack_forget()
    self.toChain.pack_forget()
    self.initiateButton.pack_forget()
    self.initiatorCheckbox.pack_forget()
    from swap import unpackMainSwapGUI
    unpackMainSwapGUI(self)

def repackMainGUI(self):
    self.fromChainLabel.pack(pady=2, padx=2)
    self.fromChain.pack(pady=2, padx=2) 
    self.toChainLabel.pack(pady=2, padx=2)
    self.toChain.pack(pady=2, padx=2)
    self.initiatorCheckbox.pack(pady=2, padx=2)
    from swap import repackMainSwapGUI
    repackMainSwapGUI(self)


#######SWAP#########
def unpackMainSwapGUI(self): #unpack and repack are bulk unpacking subroutines for GUI basic ordering
    self.initiatorCommitLabel.pack_forget()
    self.initiatorCommitment.pack_forget()
    self.responseCommitLabel.pack_forget()
    self.respondButton.pack_forget()
    self.initiateButton.pack_forget()

def repackMainSwapGUI(self):
    self.initiatorCommitLabel.pack()
    self.initiatorCommitment.pack()
    self.responseCommitLabel.pack()
    self.respondButton.pack()
    self.initiateButton.pack()

def GUI_Arrange_Swap_Based(self): #here we are updating the GUI according to the CURRENT state of the isInitiator boolean
    if self.isInitiator == True:    #Swap based arrange is a specific ordering based on the state of the initiator
        if hasattr(self, 'swap_tab_view'):
            self.swap_tab_view.pack_forget()
        self.initiatorCommitLabel.pack_forget()
        self.initiatorCommitment.pack_forget()
        self.responseCommitLabel.pack_forget()
        self.respondButton.pack_forget()
        self.initiateButton.pack()
        if hasattr(self, 'swap_tab_view'):
            self.swap_tab_view.pack()
    else:
        if hasattr(self, 'swap_tab_view'):
            self.swap_tab_view.pack_forget()

        self.initiateButton.pack_forget()
        self.initiatorCommitLabel.pack()
        self.initiatorCommitment.pack()
        self.responseCommitLabel.pack()
        self.respondButton.pack()

        if hasattr(self, 'swap_tab_view'):
            self.swap_tab_view.pack()

#######CHAIN#########
def GUI_ReArrange_Chain_Based(self):
    from GUI_manager import unpackMainGUI, repackMainGUI
    if self.senderChain == "Ergo" or self.receiverChain == "Ergo": #future make this all non account chains
        unpackMainGUI(self)                                            #TODO: current issue is that this handles swap based GUI
                                                    #coordinating accross is difficult, need to pick specific GUI order
        self.chainPubkeyLabel.pack(pady=2, padx=2)
        self.chainPubkeyEntry.pack(pady=2, padx=2) #introduce derived public key indexer for non account chains
        self.setChainPubkey.pack(pady=2, padx=2)

        repackMainGUI(self)
        from swap import GUI_Arrange_Swap_Based
        GUI_Arrange_Swap_Based(self)
    else:
        self.chainPubkeyLabel.pack_forget()
        self.chainPubkeyEntry.pack_forget()
        self.setChainPubkey.pack_forget() #remove indexer for account chains

        unpackMainGUI(self)
        repackMainGUI(self)
        from swap import GUI_Arrange_Swap_Based
        GUI_Arrange_Swap_Based(self)


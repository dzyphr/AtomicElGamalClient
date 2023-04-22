#######MAIN#########
def unpackMainGUI(self):
    self.initiatorChainLabel.pack_forget()
    self.initiatorChainOption.pack_forget() 
    self.responderChainLabel.pack_forget()
    self.responderChainOption.pack_forget()
    self.initiateButton.pack_forget()
    self.initiatorCheckbox.pack_forget()
    self.initiatorCommitLabel.pack_forget()
    self.initiatorCommitment.pack_forget()
    self.responseCommitLabel.pack_forget()
    self.respondButton.pack_forget()

def repackMainGUI(self):
    self.initiatorChainLabel.pack(pady=2, padx=2)
    self.initiatorChainOption.pack(pady=2, padx=2) 
    self.responderChainLabel.pack(pady=2, padx=2)
    self.responderChainOption.pack(pady=2, padx=2)
    self.initiatorCheckbox.pack(pady=2, padx=2)

#######SWAP#########
def unpackMainSwapGUI(self): #unpack and repack are bulk unpacking subroutines for GUI basic ordering
    self.initiatorCommitLabel.pack_forget()
    self.initiatorCommitment.pack_forget()
    self.responseCommitLabel.pack_forget()
    self.respondButton.pack_forget()
    self.initiateButton.pack_forget()

def repackMainSwapGUI(self):
    self.initiatorCommitLabel.pack(pady=2, padx=2)
    self.initiatorCommitment.pack(pady=2, padx=2)
    self.responseCommitLabel.pack(pady=2, padx=2)
    self.respondButton.pack(pady=2, padx=2)
    self.initiateButton.pack(pady=2, padx=2)

def GUI_Arrange_Swap_Based(self): #here we are updating the GUI according to the CURRENT state of the isInitiator boolean
    if self.isInitiator == True:    #Swap based arrange is a specific ordering based on the state of the initiator
        if hasattr(self, 'swap_tab_view'):
            self.swap_tab_view.pack_forget()
        self.initiatorCommitLabel.pack_forget()
        self.initiatorCommitment.pack_forget()
        self.responseCommitLabel.pack_forget()
        self.respondButton.pack_forget()
        self.initiatorChainLabel.pack(pady=2, padx=2)
        self.initiatorChainOption.pack(pady=2, padx=2)
        self.initiateButton.pack(pady=2, padx=2)
        if hasattr(self, 'swap_tab_view'):
            self.swap_tab_view.pack()
    else:
        if hasattr(self, 'swap_tab_view'):
            self.swap_tab_view.pack_forget()
        self.initiateButton.pack_forget()
        self.initiatorChainLabel.pack_forget()
        self.initiatorChainOption.pack_forget()
        self.initiatorCommitLabel.pack(pady=2, padx=2)
        self.initiatorCommitment.pack(pady=2, padx=2)
        self.responseCommitLabel.pack(pady=2, padx=2)
        self.respondButton.pack(pady=2, padx=2)
        if hasattr(self, 'swap_tab_view'):
            self.swap_tab_view.pack()

#######CHAIN#########
def GUI_ReArrange_Chain_Based(self):
    from GUI_manager import unpackMainGUI, repackMainGUI
    if self.initiatorChain == "Ergo" or self.responderChain == "Ergo" or self.crossChain == "Ergo": 
        #future make this all non account chains
        unpackMainGUI(self)                                            #TODO: current issue is that this handles swap based GUI
        self.chainPubkeyLabel.pack(pady=2, padx=2)
        self.chainPubkeyEntry.pack(pady=2, padx=2) #introduce derived public key indexer for non account chains
        if self.chainPubkeyEntry.get() == "":
            self.chainPubkeyEntry.insert(0, "0")
        repackMainGUI(self)
        from swap import GUI_Arrange_Swap_Based
        GUI_Arrange_Swap_Based(self)
    else:
        self.chainPubkeyLabel.pack_forget()
        self.chainPubkeyEntry.pack_forget() #remove pubkey index for account / evm chains
        unpackMainGUI(self)
        repackMainGUI(self)
        from swap import GUI_Arrange_Swap_Based
        GUI_Arrange_Swap_Based(self)


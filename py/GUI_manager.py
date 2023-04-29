import customtkinter
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


def setSwapTab(self, first):
    from swap import SwapTab, copyENCInit, decryptResponse
    def goCopyENCInit():
        copyENCInit(self)
    def goDecryptResponse():
        decryptResponse(self)
    if self.isInitiator == True:
        if first == True:
            self.swap_tab_view = SwapTab(master=self.frame, width=600, height=600)
            self.swap_tab_view.add(self.currentswapname)
            self.swap_tab_view.copylabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Click to copy generated Pedersen commitments: ")
            self.swap_tab_view.copylabel.grid(row=0, column=0, padx=10, pady=10)
            self.swap_tab_view.copyButton = \
                    customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Copy", command=goCopyENCInit)
            self.swap_tab_view.copyButton.grid(row=1, column=0, padx=10, pady=10)
            self.swap_tab_view.responderPasteLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Paste responders commitment: ")
            self.swap_tab_view.responderPasteLabel.grid(row=2, column=0, padx=10, pady=10)
            self.swap_tab_view.responderCommitment = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname),\
                    placeholder_text="Responder's Commitments", \
                    width=700, height=5)
            self.swap_tab_view.responderCommitment.grid(row=3, column=0, padx=10, pady=10)
            self.swap_tab_view.decryptResponderCommitmentLabel =  \
                    customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Decrypt responders commitment: ")
            self.swap_tab_view.decryptResponderCommitmentLabel.grid(row=4, column=0, padx=10, pady=10)
            self.swap_tab_view.decryptResponderCommitmentButton = \
                    customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Decrypt", command=goDecryptResponse)
            self.swap_tab_view.decryptResponderCommitmentButton.grid(row=5, column=0, padx=10, pady=10)
            self.swap_tab_view.pack()
            self.swapTabSet = True
        else:
            self.swap_tab_view.add(self.currentswapname)
            self.swap_tab_view.copylabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Click to copy generated Pedersen commitments: ")
            self.swap_tab_view.copylabel.grid(row=0, column=0, padx=10, pady=10)
            self.swap_tab_view.copyButton = \
                    customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Copy", command=goCpyENCInit)
            self.swap_tab_view.copyButton.grid(row=1, column=0, padx=10, pady=10)
            self.swap_tab_view.responderPasteLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Paste responders commitment: ")
            self.swap_tab_view.responderPasteLabel.grid(row=2, column=0, padx=10, pady=10)
            self.swap_tab_view.responderCommitment = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
                    placeholder_text="Responder's Commitments", \
                    width=700, height=5)
            self.swap_tab_view.responderCommitment.grid(row=3, column=0, padx=10, pady=10)
            self.swap_tab_view.decryptResponderCommitmentLabel =  \
                    customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Decrypt responders commitment: ")
            self.swap_tab_view.decryptResponderCommitmentLabel.grid(row=4, column=0, padx=10, pady=10)
            self.swap_tab_view.decryptResponderCommitmentButton = \
                    customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Decrypt", command=goSecryptResponse)
            self.swap_tab_view.decryptResponderCommitmentButton.grid(row=5, column=0, padx=10, pady=10)
    else:
        if first == True:
            self.swap_tab_view = SwapTab(master=self.frame, width=600, height=600)
            self.swap_tab_view.add(self.currentswapname)
            self.swap_tab_view.pack()
            self.swapTabSet = True
        else:
            self.swap_tab_view.add(self.currentswapname)

def SwapResponderGUI(self):
    from swap import copyResponse, deployAndFundScalarSwapContract
    def goCopyResponse():
        copyResponse(self)
    def goDeployAndFundScalarSwapContract():
        deployAndFundScalarSwapContract(self)
    self.swap_tab_view.valueLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
        text="Amount to spend in wei:")
    self.swap_tab_view.valueLabel.grid(row=0, column=0, padx=10, pady=10)
    self.swap_tab_view.valueToSpendEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="coin amount in wei")
    self.swap_tab_view.valueToSpendEntry.grid(row=1, column=0, padx=10, pady=10)

    self.deployAtomicSwapContractLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Click to deploy & fund the atomic swap contract: ")
    self.deployAtomicSwapContractLabel.grid(row=2, column=0, padx=10, pady=10)
    self.deployAtomicSwapButton = customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Deploy & Fund", command=goDeployAndFundScalarSwapContract)
    self.deployAtomicSwapButton.grid(row=3, column=0, padx=10, pady=10)
    self.counterpartyChainPubkeyLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Counterparty ChainPubkey: " + self.counterpartyChainPubkey)
    self.counterpartyChainPubkeyLabel.grid(row=4, column=0, padx=10, pady=10)

    #TODO: WARN USER about sending funds!!
    #TODO: make value entry based on chain aka wei or sats
    self.swap_tab_view.labelresponse = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
        text="Click to copy generated response commitments: ")
    self.swap_tab_view.labelresponse.grid(row=5, column=0, padx=10, pady=10)
    self.swap_tab_view.copyResponseButton = \
            customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Copy", command=goCopyResponse)
    self.swap_tab_view.copyResponseButton.grid(row=6, column=0, padx=10, pady=10)


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


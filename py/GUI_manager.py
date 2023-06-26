import json, os, threading, customtkinter, time, file_tools
from file_tools import clean_file_open
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
    from swap import SwapTab, copyENCInit, inspectScalarLockContract, draftFinalSignature,\
            checkTreeForFinalization, deduce_sr, getLocalLockTime, SigmaParticleRefund, updateDataBasedOnOpenTab

    def goCopyENCInit():
        copyENCInit(self)

    def goInspectScalarLockContract():
        t = threading.Thread(target=inspectScalarLockContract, args=(self,))
        t.start()

    def goDraftFinalSignature():
        t = threading.Thread(target=draftFinalSignature, args=(self,))
        t.start()

    def goCheckTreeForFinalization():
        t = threading.Thread(target=checkTreeForFinalization, args=(self,))
        t.start()

    def goDeduce_sr():
        t = threading.Thread(target=deduce_sr, args=(self,))
        t.start()

    def goCheckLockTime():
        lockTime = getLocalLockTime(self, self.currentswapname)
        if lockTime != None: 
            if int(lockTime) > 0:
                self.swap_tab_view.RefundLockTimeLabel.configure(text="Refund Lock Time Remaining: " + str(lockTime))
            else:
                self.swap_tab_view.RefundLockTimeLabel.configure(text="Refund Lock Time Remaining: 0")
                self.swap_tab_view.RefundButton.configure(state="normal")
        else:
            print("cannot check locktime, contract not confirmed on chain yet?")


    def goRefund():
        updateDataBasedOnOpenTab(self)
        f = open(self.currentswapname + "/roleData.json", "r") #TODO: This is likely the most accurate way to pick a chain responsively
        role = json.loads(f.read())["role"]
        f.close()
        if role == "initiator":
            f = open(self.currentswapname + "/initiation.atomicswap", "r")
            initiatorChain = json.loads(f.read())["localChain"]
            f.close()
            if initiatorChain == "Ergo":
                t = threading.Thread(target=SigmaParticleRefund, args=(self,))
                t.start()


#    def goDecryptResponse():`
#        decryptResponse(self)
    def InitiatorGui():
        self.swap_tab_view.copylabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Click to copy generated Pedersen commitments: ")
        self.swap_tab_view.copylabel.grid(row=0, column=0, padx=4, pady=4)
        self.swap_tab_view.copyButton = \
                customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Copy", command=goCopyENCInit, width=5, height=7)
        self.swap_tab_view.copyButton.grid(row=0, column=1, padx=4, pady=4)
        self.swap_tab_view.responderPasteLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Paste responders commitment: ")
        self.swap_tab_view.responderPasteLabel.grid(row=2, column=0, padx=4, pady=4)
        self.swap_tab_view.responderCommitment = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname),\
                placeholder_text="Responder's Commitments", \
                width= 300, height=5)
        self.swap_tab_view.responderCommitment.grid(row=3, column=0, padx=4, pady=4)
        self.swap_tab_view.decryptResponderCommitmentLabel =  \
                customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Check responders commitment: ")
        self.swap_tab_view.decryptResponderCommitmentLabel.grid(row=4, column=0, padx=4, pady=4)
        self.swap_tab_view.decryptResponderCommitmentButton = \
                customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Check", command=goInspectScalarLockContract, width=5, height=7, state="disabled")
        self.swap_tab_view.decryptResponderCommitmentButton.grid(row=4, column=1, padx=4, pady=4)
        self.swap_tab_view.responderContractValueLabel = \
                customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Responder Commitment not collected yet")
        self.swap_tab_view.responderContractValueLabel.grid(row=6, column=0, padx=4, pady=4)

        self.swap_tab_view.initiatorContractValueLabel = \
                customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Amount of nanoErg to fund contract with:")
        self.swap_tab_view.initiatorContractValueLabel.grid(row=7, column=0, padx=4, pady=4)
        self.swap_tab_view.refundDurationEntryLabel = \
                customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Lock time:")
        self.swap_tab_view.refundDurationEntryLabel.grid(row=7, column=1, padx=4, pady=4)
        self.swap_tab_view.initiatorContractValueEntry = \
                customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname),\
                placeholder_text="NanoErgs", \
                width=70, height=5)
        self.swap_tab_view.initiatorContractValueEntry.grid(row=8, column=0, padx=4, pady=4)
        self.swap_tab_view.refundDurationEntry = \
                customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname),\
                placeholder_text="25", \
                width=30, height=5)
        self.swap_tab_view.refundDurationEntry.grid(row=8, column=1, padx=4, pady=4)
        self.swap_tab_view.finalizeSwapButton = \
                customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Deploy Contract & Copy Commitment", command=goDraftFinalSignature, width=5, height=5, state="disabled")
        self.swap_tab_view.finalizeSwapButton.grid(row=9, column=0, padx=4, pady=4)
        self.swap_tab_view.finalizeCheck = \
                customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Check tree for finalization", command=goCheckTreeForFinalization, state="disabled")
        self.swap_tab_view.finalizeCheck.grid(row=10, column=0, padx=4, pady=4)
        self.swap_tab_view.InitiatorCustomGasLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="custom gas :")
        self.swap_tab_view.InitiatorCustomGasLabel.grid(row=9, column=2, padx=4, pady=4)
        self.swap_tab_view.InitiatorGasEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="8000000", width=70, height=5)
        self.swap_tab_view.InitiatorGasEntry.grid(row=10, column=2, padx=4, pady=4)
        self.swap_tab_view.InitiatorCustomGasModLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="gas mod :")
        self.swap_tab_view.InitiatorCustomGasModLabel.grid(row=9, column=3, padx=4, pady=4)
        self.swap_tab_view.InitiatorGasModEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
                placeholder_text="1", width=10, height=5)
        self.swap_tab_view.InitiatorGasModEntry.grid(row=10, column=3, padx=4, pady=4)

        self.swap_tab_view.claim = \
                customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Claim", command=goDeduce_sr, width=5, height=7, state="disabled")
        self.swap_tab_view.claim.grid(row=10, column=1, padx=4, pady=4)
        self.swap_tab_view.checkRefundLockTime = \
                customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                text="LockTime", command=goCheckLockTime, width=10, height=7, state="disabled")
        self.swap_tab_view.checkRefundLockTime.grid(row=11, column=0, padx=4, pady=4)
        self.swap_tab_view.RefundButton = \
                customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Refund",  width=10, height=7, state="disabled", command=goRefund)
        self.swap_tab_view.RefundButton.grid(row=11, column=1, padx=4, pady=4)
        self.swap_tab_view.RefundLockTimeLabel = \
                customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                text="Refund Lock Time Remaining: uninitiated")
        self.swap_tab_view.RefundLockTimeLabel.grid(row=12, column=0, padx=4, pady=4)
        self.swap_tab_view.minimumValueAutoClaim = \
            customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="minimum autoclaim val in wei", width=300, height=5) #TODO automate denomination label
        self.swap_tab_view.minimumValueAutoClaim.grid(row=13, column=0, padx=4, pady=4)
        self.swap_tab_view.autoClaimCheckbox = \
                customtkinter.CTkCheckBox(master=self.swap_tab_view.tab(self.currentswapname) \
                , text="AutoClaim")#, \
        #            command=goAutoClaimTHREAD)
        self.swap_tab_view.autoClaimCheckbox.grid(row=13, column=1, padx=4, pady=4)


    if self.isInitiator == True:
        if first == True:
            self.swap_tab_view = SwapTab(master=self.frame, width=600, height=600)
            self.swap_tab_view.add(self.currentswapname)
            InitiatorGui() 
            self.swap_tab_view.pack()
            self.swapTabSet = True
        else:
            self.swap_tab_view.add(self.currentswapname)
            InitiatorGui()

    else:
        if first == True:
            self.swap_tab_view = SwapTab(master=self.frame, width=600, height=600)
            self.swap_tab_view.add(self.currentswapname)
            self.swap_tab_view.pack()
            self.swapTabSet = True
        else:
            self.swap_tab_view.add(self.currentswapname)

def SwapResponderGUI(self):
    from swap import copyResponse, deployAndFundScalarSwapContract, responderCheck, \
            getLocalLockTime, AtomicityRefund, updateDataBasedOnOpenTab, AutoClaim, responderClaim #TODO rename receiver to responder?

    def goCopyResponse():
        t = threading.Thread(target=copyResponse, args=(self,))
        t.start()

    def goDeployAndFundScalarSwapContract():
        t = threading.Thread(target=deployAndFundScalarSwapContract, args=(self,))
        t.start()

    def goResponderCheck():
        t = threading.Thread(target=responderCheck, args=(self, self.currentswapname))
        t.start()

    def goReceiverClaim():
        t = threading.Thread(target=responderClaim, args=(self,))
        t.start()

    def goCheckLockTime():
        lockTime = getLocalLockTime(self, self.currentswapname)
        if lockTime != None:
            self.swap_tab_view.lockTimeLabel.configure(text="LockTime: " + lockTime)
            if int(lockTime) == 0:
                self.swap_tab_view.refundButton.configure(state="normal")
        else:
            print("error checking locktime")

    def goRefund():
        t = threading.Thread(target=AtomicityRefund, args=(self,))
        t.start()


    def goAutoClaim():
        updateDataBasedOnOpenTab(self)
        relevantTab = self.currentswapname
        while True:
            if os.path.isfile(relevantTab + "/AutoClaim") == False:
                print("no autoclaim file found yet creating one")
                clean_file_open(relevantTab + "/AutoClaim", "w", "true", "AutoClaim file not writable")
                self.swap_tab_view.claimButton.configure(state="disabled")
                if os.path.isfile(relevantTab + "/DEC_Finalization.atomicswap"):
                    if os.path.isfile(relevantTab + "/DEC_initiation.atomicswap") == True:
                        chain = json.loads(clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "r"))["localChain"]
                        if chain == "Ergo":
                            if os.path.isfile(relevantTab + "/InitiatorContractValue"):
                                print("autoclaiming")
                                returnVal = AutoClaim(self, relevantTab)
                                if type(returnVal) == type(None):
                                        continue
                                if type(returnVal) == type(str):
                                    if "error"  in returnVal:
                                        continue
                                else:
                                    break
                    else:
                        responderCheck(self, relevantTab)
                        time.sleep(5)
                        continue
                else:
                    print("finalization not found, waiting...")
                    time.sleep(5)
                    continue
            elif os.path.isfile(relevantTab + "/AutoClaim") == True:
                b = clean_file_open(relevantTab + "/AutoClaim", "r")
                if b == "true" and self.swap_tab_view.autoClaimCheckbox.get() == 0:
                    print("autoclaim true, changing to false")
                    clean_file_open(relevantTab + "/AutoClaim", "w", "false", "AutoClaim file not writable", truncate=True)
                    if os.path.isfile(relevantTab + "/DEC_Finalization.atomicswap"):
                        if os.path.isfile(relevantTab + "/DEC_initiation.atomicswap") == True:
                            chain = json.loads(clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "r"))["localChain"]
                            if chain == "Ergo":
                                if os.path.isfile(relevantTab + "/InitiatorContractValue"):
                                    val =  clean_file_open(relevantTab + "/InitiatorContractValue", "r")
                                    if val > 1:
                                        self.swap_tab_view.claimButton.configure(state="normal")
                                        break
                                else: 
                                    responderCheck(self, relevantTab)
                                    break
                    else:
                        break
                if b == "false" and self.swap_tab_view.autoClaimCheckbox.get() == 1:
                    print("autoclaim false, changing to true")
                    clean_file_open(relevantTab + "/AutoClaim", "w", \
                            writingContent="true", extraWarn="AutoClaim file not writable", truncate=True) 
                    self.swap_tab_view.claimButton.configure(state="disabled")
                    print("looking for " + relevantTab + "/DEC_Finalization.atomicswap" + " path")
                    if os.path.isfile(relevantTab + "/DEC_Finalization.atomicswap"):
                        print("found " + relevantTab + "/DEC_Finalization.atomicswap" + " path")
                        if os.path.isfile(relevantTab + "/DEC_initiation.atomicswap") == True:
                            chain = json.loads(clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "r"))["localChain"]
                            if chain == "Ergo":
                                print("looking for " + relevantTab + "/InitiatorContractValue" + " path")
                                if os.path.isfile(relevantTab + "/InitiatorContractValue"):
                                    print("found " + relevantTab + "/InitiatorContractValue" + " path")
                                    print("autoclaiming")
                                    returnVal = AutoClaim(self, relevantTab)
                                    if type(returnVal) == type(None):
                                        continue
                                    if type(returnVal) == type(str):
                                        if "error"  in returnVal:
                                            continue
                                    else:
                                        break
                                else:
                                    responderCheck(self, relevantTab)
                                    time.sleep(5)
                                    continue
                    else:
                        time.sleep(5)
                        continue
                if b == "true" and self.swap_tab_view.autoClaimCheckbox.get() == 1: 
                    if os.path.isfile(relevantTab + "/DEC_Finalization.atomicswap"):
                        print("found " + relevantTab + "/DEC_Finalization.atomicswap" + " path")
                        if os.path.isfile(relevantTab + "/DEC_initiation.atomicswap") == True:
                            chain = json.loads(clean_file_open(relevantTab + "/DEC_initiation.atomicswap", "r"))["localChain"]
                            if chain == "Ergo":
                                print("looking for " + relevantTab + "/InitiatorContractValue" + " path")
                                if os.path.isfile(relevantTab + "/InitiatorContractValue"):
                                    print("found " + relevantTab + "/InitiatorContractValue" + " path")
                                    print("autoclaiming")
                                    returnVal = AutoClaim(self, relevantTab)
                                    if type(returnVal) == type(None):
                                        continue
                                    if type(returnVal) == type(str):
                                        if "error"  in returnVal:
                                            continue
                                    else:
                                        break
                                else:
                                    responderCheck(self, relevantTab)
                                    time.sleep(5)
                                    continue
                    else:
                        print("finalization not found, waiting...")
                        time.sleep(5)
                        continue
                else:
                    time.sleep(5)
                    continue

    def goAutoClaimTHREAD():
        t = threading.Thread(target=goAutoClaim)
        t.start()

    self.swap_tab_view.valueLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
        text="Amount to spend in wei")
    self.swap_tab_view.valueLabel.grid(row=0, column=1, padx=4, pady=4)
    self.swap_tab_view.GasEntryLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
        text="custom gas ")
    self.swap_tab_view.GasEntryLabel.grid(row=0, column=2, padx=4, pady=4)
    self.swap_tab_view.GasModEntryLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
        text="gas mod")
    self.swap_tab_view.GasModEntryLabel.grid(row=0, column=3, padx=4, pady=4)
    self.swap_tab_view.valueToSpendEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="coin amount in wei")
    self.swap_tab_view.valueToSpendEntry.grid(row=1, column=1, padx=4, pady=4)
    self.swap_tab_view.GasEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="8000000", width=70, height=5)
    self.swap_tab_view.GasEntry.grid(row=1, column=2, padx=4, pady=4)
    self.swap_tab_view.GasModEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="1", width=5, height=5)
    self.swap_tab_view.GasModEntry.grid(row=1, column=3, padx=4, pady=4)

#   self.swap_tab_view.deployAtomicSwapContractLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
 #          text="Click to deploy & fund the atomic swap contract: ")
#   self.swap_tab_view.deployAtomicSwapContractLabel.grid(row=2, column=0, padx=4, pady=4)
    self.swap_tab_view.CustomLockTimeLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Custom LockTime")
    self.swap_tab_view.CustomLockTimeLabel.grid(row=2, column=2, padx=4, pady=4)
    self.swap_tab_view.CheckCurrentLockTimeLabel = \
            customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Check Locktime ")
    self.swap_tab_view.CheckCurrentLockTimeLabel.grid(row=2, column=3, padx=4, pady=4)
    self.swap_tab_view.deployAtomicSwapButton = customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Deploy & Fund", command=goDeployAndFundScalarSwapContract,  width=5, height=7)
    self.swap_tab_view.deployAtomicSwapButton.grid(row=3, column=1, padx=4, pady=4)
    self.swap_tab_view.CustomLockTimeEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="200", width=50, height=5)
    self.swap_tab_view.CustomLockTimeEntry.grid(row=3, column=2, padx=4, pady=4)
    self.swap_tab_view.checkLockTimeButton = customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
            text="LockTime",   width=5, height=7, command=goCheckLockTime, state="disabled")
    self.swap_tab_view.checkLockTimeButton.grid(row=3, column=3, padx=4, pady=4)
    self.swap_tab_view.lockTimeLabel =  customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
            text="LockTime: unititiated")
    self.swap_tab_view.lockTimeLabel.grid(row=4, column=2, padx=4, pady=4)
    self.swap_tab_view.refundButton = customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Refund",   width=4, height=7,  state="disabled", command=goRefund)
    self.swap_tab_view.refundButton.grid(row=4, column=3, padx=4, pady=4)

    #TODO: WARN USER about sending funds!!
    #TODO: make value entry based on chain aka wei or sats
#    self.swap_tab_view.labelresponse = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
#        text="Click to copy response : ")
#    self.swap_tab_view.labelresponse.grid(row=5, column=0, padx=4, pady=4)
    self.swap_tab_view.copyResponseButton = \
            customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Copy Response", command=goCopyResponse,  width=5, height=7, state="disabled")
    self.swap_tab_view.copyResponseButton.grid(row=5, column=1, padx=4, pady=4)
    self.swap_tab_view.labelFinalize = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
        text="Paste Finalization Commitment: ")
    self.swap_tab_view.labelFinalize.grid(row=7, column=1, padx=4, pady=4)
    self.swap_tab_view.finalizeEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="Finalization", width=300, height=5)
    self.swap_tab_view.finalizeEntry.grid(row=8, column=1, padx=4, pady=4)
    self.swap_tab_view.checkButton = \
            customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Check", command=goResponderCheck,  width=5, height=7, state="disabled") 
    self.swap_tab_view.checkButton.grid(row=8, column=2, padx=4, pady=4)
    self.swap_tab_view.labelContractAmount = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
        text="Contract amount: not checked yet")
    self.swap_tab_view.labelContractAmount.grid(row=10, column=1, padx=4, pady=4)

    self.swap_tab_view.claimButton = \
            customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Claim", command=goReceiverClaim,  width=5, height=7, state="disabled")
    self.swap_tab_view.claimButton.grid(row=10, column=2, padx=4, pady=4)
    self.swap_tab_view.counterpartyChainPubkeyLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
            text="Counterparty: " + self.counterpartyChainPubkey)
    self.swap_tab_view.counterpartyChainPubkeyLabel.grid(row=11, column=1, padx=4, pady=4)
    self.swap_tab_view.minimumValueAutoClaim = \
            customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
        placeholder_text="minimum value in nanoErg (for autoclaim)", width=300, height=5) #TODO automate denomination label
    self.swap_tab_view.minimumValueAutoClaim.grid(row=12, column=1, padx=4, pady=4)
    self.swap_tab_view.autoClaimCheckbox = \
            customtkinter.CTkCheckBox(master=self.swap_tab_view.tab(self.currentswapname) \
            , text="AutoClaim", \
                command=goAutoClaimTHREAD)
    self.swap_tab_view.autoClaimCheckbox.grid(row=12, column=2, padx=4, pady=4)




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


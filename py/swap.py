from chain import setChainPubkey, setSenderChain
import tkinter, customtkinter, os, json, time, subprocess, sys, io, pyperclip

class SwapTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


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

def setInitiator(self): #here we are setting the initiator based on the PREVIOUS state of the isInitiator boolean
    if self.isInitiator == True:
        self.isInitiator = False
        setSenderChain(self, self.fromChain.get())
        print("isInitiator = ", self.isInitiator)
        GUI_Arrange_Swap_Based(self)
    else:
        self.isInitiator = True
        print("isInitiator = ", self.isInitiator)
        setSenderChain(self, self.fromChain.get())
        GUI_Arrange_Swap_Based(self)

def determineSwapName():
    swap = "swap"
    index = 1
    strindex = str(index)
    swapname = swap + strindex
    if os.path.isdir(swapname) == False:
        print(swapname + " dir not found")
        os.mkdir(swapname)
    else:
        while True:
            index = index + 1
            strindex = str(index)
            swapname = swap + strindex
            if os.path.isdir(swapname) == False:
                os.mkdir(swapname)
                print("making dir " + swapname )
                break
    return swapname

def initiateSwap(self):
    def copyENCInit():
            pyperclip.copy(open(self.swap_tab_view.get() + "/ENC_initiation.atomicswap", "r").read()) 
            #make sure active tab functions get swap name from current open tab
    if self.senderChain  == "NotSelected" or self.receiverChain == "NotSelected":
        print("at least one chain not selected!")
    elif self.senderChain == self.receiverChain:
        print("same chain selected for both sides of swap!")
    else:
        self.currentReceiver = self.CounterpartyElGamalKey.get()
        if self.currentReceiver == "":
            print("receiver ElGamal Key not specified!")
        elif len(self.currentReceiver) < 616:
            print("receiver ElGamal Key is less than 2048 bit")
        elif any(c.isalpha() for c in self.currentReceiver):
            print("detected alphabetical characters, hexadecimal keys not implemented yet")
        elif self.isInitiator == True:
            if self.chainPubkey == "":
                setChainPubkey(self)
            self.currentswapname = determineSwapName()
            if self.swapTabSet == False:
                self.swap_tab_view = SwapTab(master=self.frame, width=600, height=600)
                self.swap_tab_view.add(self.currentswapname)
                self.swap_tab_view.label = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Click to copy generated Pedersen commitments: ")
                self.swap_tab_view.label.grid(row=0, column=0, padx=10, pady=10)
                self.swap_tab_view.newElGamalKeyButton = \
                        customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Copy", command=copyENCInit)
                self.swap_tab_view.newElGamalKeyButton.grid(row=1, column=0, padx=10, pady=10) #ElGamal KeyGen Button
                self.swap_tab_view.pack()
                self.swapTabSet = True
            else:
                self.swap_tab_view.add(self.currentswapname)
                self.swap_tab_view.label = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Click to copy generated Pedersen commitments: ")
                self.swap_tab_view.label.grid(row=0, column=0, padx=10, pady=10)
                self.swap_tab_view.newElGamalKeyButton = \
                        customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Copy", command=copyENCInit)
                self.swap_tab_view.newElGamalKeyButton.grid(row=1, column=0, padx=10, pady=10) #ElGamal KeyGen Button

            initiation = os.popen("python3 -u AtomicMultiSigECC/py/deploy.py  p1Initiate " + self.chainPubkey).read() #run wit -u for unbuffered stream
            runElGamal = "./ElGamal encryptToPubKey " + \
                    self.currentReceiver + ' ' + \
                    self.ElGamalKeyFileName + ' ' + \
                    "\'" + initiation + "\' " + \
                    self.currentswapname + "/ENC_initiation.atomicswap "

            encryption = os.popen(runElGamal).read()
            f = open(self.currentswapname + "/initiation.atomicswap", "w")
            f.write(initiation)
            f.close()
            f = open(self.currentswapname + "/Receiver.ElGamalPub", "w")
            f.write(self.currentReceiver)
            f.close()
            f = open(self.currentswapname + "/SenderKey.ElGamalPub", "w")
            #maybe we can just backup the whole private keyfile in this instance
            f.write(self.ElGamalPublicKey)
            f.close()
        elif self.isInitiator == False:
            def copyResponse():
                pyperclip.copy(open(self.swap_tab_view.get() + "/ENC_response_commitment.atomicswap", "r").read())
            #make sure active tab functions get swap name from current open tab
            self.currentswapname = determineSwapName()
            if self.swapTabSet == False:
                self.swap_tab_view = SwapTab(master=self.frame, width=600, height=600)
                self.swap_tab_view.add(self.currentswapname)
                self.swap_tab_view.pack()
                self.swapTabSet = True
            else:
                self.swap_tab_view.add(self.currentswapname)
            if self.initiatorCommitment.get() != "":
                f = open(self.currentswapname + "/initiation.atomicswap", "w")
                f.write(self.initiatorCommitment.get())
                f.close()
                decryptElGamal = \
                        "./ElGamal decryptFromPubKey " + self.currentswapname + "/initiation.atomicswap " + \
                        self.currentReceiver + ' ' + self.ElGamalKeyFileName
                decryption = os.popen(decryptElGamal).read()
                f = open(self.currentswapname + "/DEC_initiation.atomicswap", "w")
                f.write(decryption)
                f.close()
                j = json.loads(decryption)
                self.counterpartyChainPubkey = j["chainPubkey"]
                ksG = j["ksG"]
                response = os.popen("python3 -u AtomicMultiSigECC/py/deploy.py p2Respond " + "'" + ksG + "'").read() 
                f = open(self.currentswapname + "/response_commitment.atomicswap", "w")
                f.write(response)
                f.close()
                j = json.loads(response)
                print("you must lock the swap offer to:\n" + j["xG"] + "\nand chainPubkey:\n" + self.counterpartyChainPubkey)
                #save this into the current tab 
                runElGamal = "./ElGamal encryptToPubKey " + \
                    self.currentReceiver + ' ' + \
                    self.ElGamalKeyFileName + ' ' + \
                    "\'" + response + "\' " + \
                    self.currentswapname + "/ENC_response_commitment.atomicswap "
                encryption = os.popen(runElGamal).read()
                self.counterpartyChainPubkeyLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Counterparty ChainPubkey: " + self.counterpartyChainPubkey)
                self.counterpartyChainPubkeyLabel.grid(row=0, column=0, padx=10, pady=10)
                self.swap_tab_view.label = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Click to copy generated response commitments: ")
                self.swap_tab_view.label.grid(row=1, column=0, padx=10, pady=10)
                self.swap_tab_view.copyResponseButton = \
                        customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Copy", command=copyResponse)
                self.swap_tab_view.copyResponseButton.grid(row=2, column=0, padx=10, pady=10)
            else:
                print("paste in the encrypted initiator commitment")


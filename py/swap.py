import tkinter, customtkinter, os, json, time, subprocess, sys, io, pyperclip

class SwapTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

def setInitiator(self):
    if self.isInitiator == True:
        self.initiateButton.pack_forget()
        self.isInitiator = False
        self.initiatorCommitLabel.pack()
        self.initiatorCommitment.pack()
        self.responseCommitLabel.pack()
        self.respondButton.pack()
    else:
        self.isInitiator = True
        self.initiateButton.pack()
        self.respondButton.pack_forget()
        self.initiatorCommitLabel.pack_forget()
        self.initiatorCommitment.pack_forget()
        self.responseCommitLabel.pack_forget()

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
            pyperclip.copy(open(self.initiation_tab_view.get() + "/ENC_initiation.atomicswap", "r").read()) 
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
            self.currentswapname = determineSwapName()
            if self.swapTabSet == False:
                self.initiation_tab_view = SwapTab(master=self.frame, width=600, height=600)
                self.initiation_tab_view.add(self.currentswapname)
                self.initiation_tab_view.pack()
                self.initiation_tab_view.label = customtkinter.CTkLabel(master=self.initiation_tab_view.tab(self.currentswapname), \
                    text="Click to copy Generated Pedersen Commitments: ")
                self.initiation_tab_view.label.grid(row=0, column=0, padx=10, pady=10)
                self.initiation_tab_view.newElGamalKeyButton = \
                        customtkinter.CTkButton(master=self.initiation_tab_view.tab(self.currentswapname), \
                        text="Copy", command=copyENCInit)
                self.initiation_tab_view.newElGamalKeyButton.grid(row=1, column=0, padx=10, pady=10) #ElGamal KeyGen Button
                self.initiationTabSet = True
            else:
                self.initiation_tab_view.add(self.currentswapname)
                self.initiation_tab_view.label = customtkinter.CTkLabel(master=self.initiation_tab_view.tab(self.currentswapname), \
                    text="Click to copy Generated Pedersen Commitments: ")
                self.initiation_tab_view.label.grid(row=0, column=0, padx=10, pady=10)
                self.initiation_tab_view.newElGamalKeyButton = \
                        customtkinter.CTkButton(master=self.initiation_tab_view.tab(self.currentswapname), \
                        text="Copy", command=copyENCInit)
                self.initiation_tab_view.newElGamalKeyButton.grid(row=1, column=0, padx=10, pady=10) #ElGamal KeyGen Button

            initiation = os.popen("python3 -u AtomicMultiSigECC/py/deploy.py p1Initiate").read() #run wit -u for unbuffered stream
            #to get stuff from plaintext swapfiles use json LOADS, then select by key
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
            self.currentswapname = determineSwapName()
            if self.swapTabSet == False:
                self.responder_tab_view = SwapTab(master=self.frame, width=600, height=600)
                self.responder_tab_view.add(self.currentswapname)
                self.responder_tab_view.pack()
                self.responseTabSet = True
            else:
                self.responder_tab_view.add(self.currentswapname)
            f = open(self.currentswapname + "/initiation.atomicswap", "w")
            f.write(self.initiatorCommitment.get())
            f.close()
            decryptElGamal = \
                    "./ElGamal decryptFromPubKey " + self.currentswapname + "/initiaton.atomicswap " + \
                    self.currentReceiver + ' '+ self.ElGamalKeyFileName
            print(decryptElGamal)

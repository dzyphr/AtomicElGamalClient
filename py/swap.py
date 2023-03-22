import tkinter, customtkinter, os, json, time, subprocess, sys, io
class SwapTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        swapname = "swap 1"
        self.add(swapname)
        self.label = customtkinter.CTkLabel(master=self.tab(swapname), text="Generated Pedersen Commitments: ")
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.rslabel = customtkinter.CTkLabel(master=self.tab(swapname), text="rs: ")
        self.rslabel.grid(row=2, column=0, padx=10, pady=1)
        self.kslabel = customtkinter.CTkLabel(master=self.tab(swapname), text="ks: ")
        self.kslabel.grid(row=3, column=0, padx=10, pady=1)
        self.rsGlabel = customtkinter.CTkLabel(master=self.tab(swapname), text="rsG: ")
        self.rsGlabel.grid(row=4, column=0, padx=10, pady=1)
        self.ksGlabel = customtkinter.CTkLabel(master=self.tab(swapname), text="ksG: ")
        self.ksGlabel.grid(row=5, column=0, padx=10, pady=1)


def setInitiator(self):
    if self.isInitiator == True:
        self.initiateButton.pack_forget()
        self.isInitiator = False
    else:
        self.isInitiator = True
        self.initiateButton.pack()

def initiateSwap(self):
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
        else:
            self.tab_view = SwapTab(master=self.frame, width=600, height=600)
            self.tab_view.pack()
            os.mkdir("swap1") #TODO: swapname modularity
            initiation = os.popen("python3 -u AtomicMultiSigECC/py/deploy.py p1Initiate").read() #run wit -u for unbuffered stream
            self.tab_view.rslabel.configure(text="rs: " + json.loads(initiation)["rs"])
            self.tab_view.kslabel.configure(text="ks: " + json.loads(initiation)["ks"])
            self.tab_view.rsGlabel.configure(text="rsG: " + json.loads(initiation)["rsG"])
            self.tab_view.ksGlabel.configure(text="ksG: " + json.loads(initiation)["ksG"])
            f = open("swap1/initiation.atomicswap", "w")
            f.write(initiation)
            f.close()
            f = open("swap1/Receiver.ElGamalPub", "w")
            f.write(self.currentReceiver)
            f.close()
            f = open("swap1/SenderKey.ElGamalPub", "w")#maybe we can just backup the whole private keyfile in this instance
            f.write(self.ElGamalPublicKey)
            f.close()
            print(initiation)

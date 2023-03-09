import tkinter, customtkinter, os, json, time
import threading
from concurrent import futures
from threading import Thread
from ElGamalManagement import *
from chain import *
from swap import *

class GUI(customtkinter.CTk):
    def __init__(self):
        self.thread_pool_executor = futures.ThreadPoolExecutor(max_workers=4)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        root = customtkinter.CTk()
        root.geometry("1400x1200")

        self.frame = customtkinter.CTkFrame(master=root)
        self.frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        self.ElGamalPublicKey = ""
        self.keyDict = {}
        self.thisDir = os.listdir(".")
        dirElGamalKeysGetLast(self)
        firstElGamalKey(self)
        
        self.ElGamalPub = customtkinter.CTkLabel( master=self.frame, text="ElGamal PubKey: "+self.ElGamalPublicKey,font=("Roboto", 12)) 
        self.ElGamalPub.pack(padx=0.5, pady=0.5)

        def goGenElGamalKey(): #exposes ElGamal KeyGen to self 
            genNewElGamalKey(self)                                     
        newElGamalKeyButton = customtkinter.CTkButton(master=self.frame, text="New ElGamal Key", command=goGenElGamalKey)
        newElGamalKeyButton.pack(padx=20, pady=10) #ElGamal KeyGen Button

        title = customtkinter.CTkLabel( \
            master=self.frame, \
            text="ElGamal Atomic Swap Client", \
            font=("Roboto", 24)) \
            .pack(pady=12, padx=10)
        self.EnterCounterpartysKeyLabel = customtkinter.CTkLabel( master=self.frame, text="Enter Counterparty's ElGamal PubKey:")
        self.EnterCounterpartysKeyLabel.pack()
        self.CounterpartyElGamalKey = customtkinter.CTkEntry(master=self.frame, placeholder_text="Counterparty's ElGamal PubKey", \
                width=700, height=5)
        self.CounterpartyElGamalKey.pack()
        
        #sender chain dropdown
        self.senderChain = "NotSelected"
        fromChainLabel = customtkinter.CTkLabel(master=self.frame, text="Select your chain:", font=("Roboto", 14)).pack(pady=12,padx=10)
        def goSetSenderChain(choice):
            setSenderChain(self, choice)
        self.fromChain = customtkinter.CTkOptionMenu(master=self.frame, values=chains, command=goSetSenderChain)
        self.fromChain.pack(padx=20, pady=10)
       

        #receiver chain dropdown
        self.receiverChain = "NotSelected"
        toChainLabel = customtkinter.CTkLabel(master=self.frame, text="Select P2's chain:", font=("Roboto", 14)).pack(pady=12, padx=10)
        def goSetReceiverChain(choice):
            setReceiverChain(self, choice)
        self.toChain = customtkinter.CTkOptionMenu(master=self.frame, values=chains, command=goSetReceiverChain)
        self.toChain.pack(padx=20, pady=10)

        def goInitiateSwap():
            initiateSwap(self)
        self.initiateButton = customtkinter.CTkButton(master=self.frame, text="Initiate Swap", command=goInitiateSwap)

        #isInitiator Checkbox
        self.isInitiator = False
       
        def goSetInitiator():
            setInitiator(self)
        initiatorCheckbox = customtkinter.CTkCheckBox(master=self.frame, text="Are you the Swap Initiator:", command=goSetInitiator)
        initiatorCheckbox.pack(padx=20, pady=10)
        root.mainloop()     

if __name__ == "__main__":
    GUI.__init__(GUI)
    

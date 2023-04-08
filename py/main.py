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
        root.geometry("800x1000")

        self.frame = customtkinter.CTkFrame(master=root)
        self.frame.pack(pady=20, padx=30, fill="both", expand=True)
      
        self.ElGamalPublicKey = ""
        self.ElGamalPub = customtkinter.CTkLabel( master=self.frame, text="ElGamal Key File: ",font=("Roboto", 12))
        self.keyDict = {}
        self.thisDir = os.listdir(".")
        if firstElGamalKey(self) == False:
            self.ElGamalKeyFileName = dirElGamalKeysGetLast(self)
    
        
        self.ElGamalPub = customtkinter.CTkLabel( master=self.frame, \
                text="ElGamal Key File: " + self.ElGamalKeyFileName,font=("Roboto", 12))
        self.ElGamalPub.pack(pady=2, padx=2)

        def goGenElGamalKey(): #exposes ElGamal KeyGen to self 
            genNewElGamalKey(self)                                     
        newElGamalKeyButton = customtkinter.CTkButton(master=self.frame, text="New ElGamal Key", command=goGenElGamalKey)
        newElGamalKeyButton.pack(pady=2, padx=2) #ElGamal KeyGen Button

        title = customtkinter.CTkLabel( \
            master=self.frame, \
            text="ElGamal Atomic Swap Client", \
            font=("Roboto", 24)) \
            .pack(pady=2, padx=2)
        self.EnterCounterpartysKeyLabel = customtkinter.CTkLabel( master=self.frame, text="Enter Counterparty's ElGamal PubKey:")
        self.EnterCounterpartysKeyLabel.pack(pady=2, padx=2)
        self.CounterpartyElGamalKey = customtkinter.CTkEntry(master=self.frame, placeholder_text="Counterparty's ElGamal PubKey", \
                width=700, height=5)
        self.CounterpartyElGamalKey.pack(pady=2, padx=2)
       

        def goSetChainPubkey(): #TODO: we can replace all of this with deriving the pubkey from the private key based on the chain
            setChainPubkey(self)
        self.chainPubkey = ""
        self.chainPubkeyLabel =  customtkinter.CTkLabel(master=self.frame, text="Your Chain Pubkey Index:", font=("Roboto", 14))
        self.chainPubkeyLabel.pack(pady=2, padx=2)
        self.chainPubkeyLabel.pack_forget()
        self.chainPubkeyEntry = customtkinter.CTkEntry(master=self.frame, width=20, height=5)
        self.chainPubkeyEntry.pack(pady=2, padx=2)
        self.chainPubkeyEntry.pack_forget()
        self.setChainPubkey = customtkinter.CTkButton(master=self.frame, text="Set Chain Pubkey", command=goSetChainPubkey)
        self.setChainPubkey.pack(pady=2, padx=2)
        self.setChainPubkey.pack_forget()



        #sender chain dropdown
        self.senderChain = "NotSelected"
        self.fromChainLabel = customtkinter.CTkLabel(master=self.frame, text="Select your chain:", font=("Roboto", 14))
        self.fromChainLabel.pack(pady=2, padx=2)
        def goSetSenderChain(choice):
            setSenderChain(self, choice)
        self.fromChain = customtkinter.CTkOptionMenu(master=self.frame, values=chains, command=goSetSenderChain)
        self.fromChain.pack(pady=2, padx=2)

        #receiver chain dropdown
        self.receiverChain = "NotSelected"
        self.toChainLabel = customtkinter.CTkLabel(master=self.frame, text="Select P2's chain:", font=("Roboto", 14))
        self.toChainLabel.pack(pady=2, padx=2)
        def goSetReceiverChain(choice):
            setReceiverChain(self, choice)
        self.toChain = customtkinter.CTkOptionMenu(master=self.frame, values=chains, command=goSetReceiverChain)
        self.toChain.pack(pady=2, padx=2)

        def goInitiateSwap():
            initiateSwap(self)
        self.initiateButton = customtkinter.CTkButton(master=self.frame, text="Initiate Swap", command=goInitiateSwap)
        
        #isInitiator Checkbox
        self.isInitiator = False
       
        def goSetInitiator():
            setInitiator(self)
        self.initiatorCheckbox = customtkinter.CTkCheckBox(master=self.frame, text="<-- Check if you are the Initiatior", \
                command=goSetInitiator)
        self.initiatorCheckbox.pack(pady=2, padx=2)

        self.swapTabSet = False
       #responder stuff

        self.initiatorCommitLabel = customtkinter.CTkLabel(master=self.frame, \
                text="Paste the Initiator's Generated Pedersen Commitments: ")
        self.initiatorCommitLabel.pack(pady=2, padx=2)
        self.initiatorCommitment = customtkinter.CTkEntry(master=self.frame, placeholder_text="Initiator's Commitments", \
                width=700, height=5)
        self.initiatorCommitment.pack(pady=2, padx=2)
        self.responseCommitLabel = customtkinter.CTkLabel(master=self.frame, text="Click to generate response commitment: ")
        self.responseCommitLabel.pack(pady=2, padx=2)
        self.respondButton = customtkinter.CTkButton(master=self.frame, text="Respond to Swap", command=goInitiateSwap)
        self.respondButton.pack(pady=2, padx=2)




        root.mainloop()     

if __name__ == "__main__":
    GUI.__init__(GUI)
    

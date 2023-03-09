import tkinter, customtkinter, os, json, time

chains = ["NotSelected", "Ergo", "Goerli"]

def setSenderChain(self, choice):
    self.senderChain = choice
    print(self.senderChain)

def setReceiverChain(self, choice):
    self.receiverChain = choice
    print(self.receiverChain)


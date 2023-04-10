
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

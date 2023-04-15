import ast
from GUI_manager import *
from chain import setLocalChainPubkey, setCrossChainPubkey
import tkinter, customtkinter, os, json, time, subprocess, sys, io, pyperclip

class SwapTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

def setInitiator(self): #here we are setting the initiator based on the PREVIOUS state of the isInitiator boolean
    if self.isInitiator == True:
        self.isInitiator = False
#        setSenderChain(self, self.initiatorChainOption.get())
        print("isInitiator = ", self.isInitiator)
        GUI_Arrange_Swap_Based(self)
    else:
        self.isInitiator = True
        print("isInitiator = ", self.isInitiator)
#        setSenderChain(self, self.initiatorChainOption.get())
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
    if self.initiatorChainOption  == "NotSelected" or self.responderChain == "NotSelected":
        print("at least one chain not selected!")
    elif self.initiatorChainOption == self.responderChain:
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
                setCrossChainPubkey(self)
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
            init = "python3 -u AtomicMultiSigECC/py/deploy.py  p1Initiate " + self.chainPubkey
            print(init)
            initiation = os.popen(init).read() #run wit -u for unbuffered stream
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
                print(decryptElGamal)
                decryption = os.popen(decryptElGamal).read()
                f = open(self.currentswapname + "/DEC_initiation.atomicswap", "w")
                f.write(decryption)
                f.close()
                print(decryption)
                time.sleep(2)
                j = json.loads(decryption)
                self.counterpartyChainPubkey = j["chainPubkey"]
                ksG = j["ksG"]
                response = os.popen("python3 -u AtomicMultiSigECC/py/deploy.py p2Respond " + "'" + ksG + "'").read() 
                f = open(self.currentswapname + "/response_commitment.atomicswap", "w")
                f.write(response)
                f.close()
                j = json.loads(response)
                print("you must lock the swap offer to:\n" + j["xG"] + "\nand chainPubkey:\n" + self.counterpartyChainPubkey)
                cmd = "cd Atomicity && ./new_frame " + self.currentswapname  + \
                        " -M -CA 3 " + "\\\"" + self.counterpartyChainPubkey + "\\\" " \
                        + str(ast.literal_eval(j["xG"])[0])  + " " + str(ast.literal_eval(j["xG"])[1])
                print(cmd)
                new_frame = os.popen(cmd)
                time.sleep(2) #wait for file to be built
                #
                #copy in generic ECC timelock multisig contract for atomic swap
                os.remove("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol")
                contract_copy = \
                        "cd Atomicity/" + self.currentswapname + "/contracts " + \
                        "&& cp ../../AtomicMultiSigSecp256k1/contracts/AtomicMultiSigSecp256k1.sol " + self.currentswapname + ".sol" + \
                        "&& cp ../../AtomicMultiSigSecp256k1/contracts/ReentrancyGuard.sol . " + \
                        "&& cp ../../AtomicMultiSigSecp256k1/contracts/EllipticCurve.sol . "
                cpy = os.popen(contract_copy).read()
#                print(cpy)
                time.sleep(1)
                rename = str(open("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol", "r").read() )
#                print(rename.replace('AtomicMultiSigSecp256k1', self.currentswapname))
                rewrite = open("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol", "w")
                rewrite.write(rename.replace('AtomicMultiSigSecp256k1', self.currentswapname))
                specifyChain = os.popen("echo 'CurrentChain=\"" + self.responderChainOption.get() + "\"' >> Atomicity/" + \
                        self.currentswapname + "/.env").read()
                self.deployAtomicSwapContractLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Click to deploy the atomic swap contract: ")
                self.deployAtomicSwapContractLabel.grid(row=0, column=0, padx=10, pady=10)
                def deployScalarSwapContract():
                    print(os.popen("cd Atomicity/" + self.currentswapname + "/ && python3 py/deploy.py").read())
                self.deployAtomicSwapButton = customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Deploy", command=deployScalarSwapContract)
                self.deployAtomicSwapButton.grid(row=1, column=0, padx=10, pady=10)
                #save this into the current tab 
                runElGamal = "./ElGamal encryptToPubKey " + \
                    self.currentReceiver + ' ' + \
                    self.ElGamalKeyFileName + ' ' + \
                    "\'" + response + "\' " + \
                    self.currentswapname + "/ENC_response_commitment.atomicswap "
                encryption = os.popen(runElGamal).read()
                self.counterpartyChainPubkeyLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Counterparty ChainPubkey: " + self.counterpartyChainPubkey)
                self.counterpartyChainPubkeyLabel.grid(row=2, column=0, padx=10, pady=10)
                self.swap_tab_view.label = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Click to copy generated response commitments: ")
                self.swap_tab_view.label.grid(row=3, column=0, padx=10, pady=10)
                self.swap_tab_view.copyResponseButton = \
                        customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Copy", command=copyResponse)
                self.swap_tab_view.copyResponseButton.grid(row=4, column=0, padx=10, pady=10)
            else:
                print("paste in the encrypted initiator commitment")


import ast
from GUI_manager import *
from chain import setLocalChainPubkeyManual, setCrossChainPubkeyManual, setCrossChainPubkeyDerived
import tkinter, customtkinter, os, json, time, subprocess, sys, io, pyperclip

class SwapTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

def setInitiator(self): #here we are setting the initiator based on the PREVIOUS state of the isInitiator boolean
    if self.isInitiator == True:
        self.isInitiator = False
        print("isInitiator = ", self.isInitiator)
        GUI_Arrange_Swap_Based(self)
        GUI_ReArrange_Chain_Based(self)
    else:
        self.isInitiator = True
        print("isInitiator = ", self.isInitiator)
        GUI_Arrange_Swap_Based(self)
        GUI_ReArrange_Chain_Based(self)

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
    def decryptResponse():
        if os.path.isfile(self.currentswapname + "/response.atomicswap"):
            print("response commitment already collected for ", self.currentswapname)
        else:
            if self.swap_tab_view.responderCommitment.get() != "":
                responseFile = open(self.currentswapname + "/response.atomicswap", "w")
                responseFile.write(self.swap_tab_view.responderCommitment.get())
                decryptElGamal = \
                            "./ElGamal decryptFromPubKey " + self.currentswapname + "/response.atomicswap " + \
                            self.currentReceiver + ' ' + self.ElGamalKeyFileName
                decrypt = os.popen(decryptElGamal).read()
                print(decrypt)
    if self.isInitiator == True and self.initiatorChainOption  == "NotSelected" or self.responderChain == "NotSelected":
        print("at least one chain not selected! initiator must select both chains")
    elif self.isInitiator == False and self.responderChainOption  == "NotSelected":
        print("select the chain you are on!")
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
                setCrossChainPubkeyManual(self)
            self.currentswapname = determineSwapName()
            if self.swapTabSet == False:
                self.swap_tab_view = SwapTab(master=self.frame, width=600, height=600)
                self.swap_tab_view.add(self.currentswapname)
                self.swap_tab_view.copylabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Click to copy generated Pedersen commitments: ")
                self.swap_tab_view.copylabel.grid(row=0, column=0, padx=10, pady=10)
                self.swap_tab_view.copyButton = \
                        customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Copy", command=copyENCInit)
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
                        text="Decrypt", command=decryptResponse)
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
                        text="Copy", command=copyENCInit)
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
                        text="Decrypt", command=decryptResponse)
                self.swap_tab_view.decryptResponderCommitmentButton.grid(row=5, column=0, padx=10, pady=10)
                
            init = "python3 -u AtomicMultiSigECC/py/deploy.py  p1Initiate " + self.chainPubkey + " " + self.initiatorChain
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
            def copyResponse(): #Left off here
                if os.path.isfile(self.currentswapname + "/responderContractAddress"):
                    if os.path.isfile(self.swap_tab_view.get() + "/response_commitment.atomicswap"):
                        addr = open(self.currentswapname + "/responderContractAddress", "r").read().rstrip()
                        response = open(self.swap_tab_view.get() + "/response_commitment.atomicswap", "r").read() 
                        if "chain" not in response or "enter pubkey index as argument [0 - 9 for now]" in response:
                            f = open(self.currentswapname + "/response_commitment.atomicswap", "w")
                            init = open(self.currentswapname + "/DEC_initiation.atomicswap", "r").read()
                            j = json.loads(init)
                            self.counterpartyChainPubkey = j["chainPubkey"]
                            self.crossChain = j["localChain"] 
                            if self.crossChain == "Ergo": #TODO: any non account chain
                                if self.chainPubkeyEntry.get == "":
                                    self.chainPubkeyEntry.insert(0, "0")
                                    print("pubkey index not specified using 0")
                            setCrossChainPubkeyDerived(self)
                            GUI_ReArrange_Chain_Based(self)
                            edit = response.replace(\
                                    "}", \
                                    "    \"contractAddr\": " + "\"" + addr.rstrip() + "\"" + ",\n"  + \
                                    "    \"chain\": " + "\"" + self.responderChain.rstrip() + "\"" + ",\n" + \
                                    "    \"Ergo_chainPubkey: " + "\"" + self.chainPubkey.rstrip() + "\"" + "\n" + \
                                    "}")
                            f.write(edit)
                            print(edit)
                            f.close()
                            time.sleep(1)
                            runElGamal = "./ElGamal encryptToPubKey " + \
                                self.currentReceiver + ' ' + \
                                self.ElGamalKeyFileName + ' ' + \
                                "\'" + edit + "\' " + \
                                self.currentswapname + "/ENC_response_commitment.atomicswap"
                            print(runElGamal)
                            ElGamal = os.popen(runElGamal).read()
                            print(ElGamal)
                            f = open(self.currentswapname + "/ENC_response_commitment.atomicswap", "r")
                            enc_response = f.read()
                            f.close()
                            pyperclip.copy(enc_response)
                else:
                    print("swap contract not deployed yet!")

            def deployScalarSwapContract():
                    addr = os.popen("cd Atomicity/" + self.currentswapname + "/ && python3 py/deploy.py").read()
                    print(addr)
                    addrfile = open(self.currentswapname + "/responderContractAddress", "w")
                    addrfile.write(addr)
                    addrfile.close()

            def goFund():
                    if os.path.isfile(self.currentswapname + "/responderContractAddress"):
                        addr = open(self.currentswapname + "/responderContractAddress", "r").read().rstrip()
                        cmd = "cd Atomicity/" + \
                                self.currentswapname + " && ./deploy.sh sendAmount " + \
                                self.swap_tab_view.valueToSpendEntry.get()  + ' '+ addr
                        print(cmd)
                        os.popen(cmd).read()          
                    else:
                        print("responders contract not found! not deployed yet or recieved")

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
                print(decryption)
                f = open(self.currentswapname + "/DEC_initiation.atomicswap", "w")
                f.write(decryption)
                f.close()
                time.sleep(1)
                j = json.loads(decryption)
                self.counterpartyChainPubkey = j["chainPubkey"]
                ksG = j["ksG"]
                self.crossChain = j["localChain"] #When responder sending chainpubkey to counterparty, get key from this chain
                setCrossChainPubkeyDerived(self)
                GUI_ReArrange_Chain_Based(self)
                response = os.popen("python3 -u AtomicMultiSigECC/py/deploy.py p2Respond " + "'" + ksG + "'").read() 
                f = open(self.currentswapname + "/response_commitment.atomicswap", "w")
                f.write(response)
                f.close()
                j = json.loads(response)
                print("you must lock the swap offer to:\n" + j["xG"] + "\nand chainPubkey:\n" + self.counterpartyChainPubkey)
                cmd = "cd Atomicity && ./new_frame " + self.currentswapname  + \
                        " -M -CA 3 " + "\\\"" + self.counterpartyChainPubkey + "\\\" " \
                        + str(ast.literal_eval(j["xG"])[0])  + " " + str(ast.literal_eval(j["xG"])[1])
                new_frame = os.popen(cmd)
                time.sleep(1) #wait for file to be built
                #
                #copy in generic ECC timelock multisig contract for atomic swap
                os.remove("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol")
                contract_copy = \
                        "cd Atomicity/" + self.currentswapname + "/contracts " + \
                        "&& cp ../../AtomicMultiSigSecp256k1/contracts/AtomicMultiSigSecp256k1.sol " + self.currentswapname + ".sol" + \
                        "&& cp ../../AtomicMultiSigSecp256k1/contracts/ReentrancyGuard.sol . " + \
                        "&& cp ../../AtomicMultiSigSecp256k1/contracts/EllipticCurve.sol . "
                cpy = os.popen(contract_copy).read()
                time.sleep(1)
                rename = str(open("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol", "r").read() )
                rewrite = open("Atomicity/" + self.currentswapname + "/contracts/" + self.currentswapname + ".sol", "w")
                rewrite.write(rename.replace('AtomicMultiSigSecp256k1', self.currentswapname))
                rewrite.close()
                specifyChain = os.popen("echo 'CurrentChain=\"" + self.responderChainOption.get() + "\"' >> Atomicity/" + \
                        self.currentswapname + "/.env").read()
                self.deployAtomicSwapContractLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Click to deploy the atomic swap contract: ")
                self.deployAtomicSwapContractLabel.grid(row=0, column=0, padx=10, pady=10)
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

                #TODO: WARN USER about sending funds!!
                #TODO: make value entry based on chain aka wei or sats
                self.swap_tab_view.valueLabel = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Amount to spend in wei:")
                self.swap_tab_view.valueLabel.grid(row=5, column=0, padx=10, pady=10)
                self.swap_tab_view.valueToSpendEntry = customtkinter.CTkEntry(master=self.swap_tab_view.tab(self.currentswapname), \
                    placeholder_text="coin amount in wei")
                self.swap_tab_view.valueToSpendEntry.grid(row=6, column=0, padx=10, pady=10)
                self.swap_tab_view.fundButton = customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Fund", command=goFund)
                self.swap_tab_view.fundButton.grid(row=6, column=1, padx=10, pady=10)
                self.swap_tab_view.labelresponse = customtkinter.CTkLabel(master=self.swap_tab_view.tab(self.currentswapname), \
                    text="Click to copy generated response commitments: ")
                self.swap_tab_view.labelresponse.grid(row=3, column=0, padx=10, pady=10)
                self.swap_tab_view.copyResponseButton = \
                        customtkinter.CTkButton(master=self.swap_tab_view.tab(self.currentswapname), \
                        text="Copy", command=copyResponse)
                self.swap_tab_view.copyResponseButton.grid(row=4, column=0, padx=10, pady=10)
            else:
                print("paste in the encrypted initiator commitment")


import os
import subprocess
from GUI_manager import *

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


def updateDataBasedOnOpenTab(self):
    if hasattr(self, "swap_tab_view"):
        self.currentswapname = self.swap_tab_view.get()
    if os.path.isdir(self.currentswapname) == True:
        #roledata
        f = open(self.currentswapname + "/roleData.json", "r")
        role = f.read()
        f.close()
        if role == "initiator":
            self.isInitiator == True
        elif role == "responder":
            self.isInitiator == False

def saveRole(self):
    if self.isInitiator == True:
        f = open(self.currentswapname + "/roleData.json", "w")
        f.write("{\n" +
                "    \"role\": \"initiator\"\n" +
                "}")
        f.close()
    else:
        f = open(self.currentswapname + "/roleData.json", "w")
        f.write("{\n" +
                "    \"role\": \"responder\"\n" +
                "}")
        f.close()

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

def getLocalLockTime(self): #for refunds #returns lock time in # of blocks
    updateDataBasedOnOpenTab(self)
    f = open(self.currentswapname + "/roleData.json", "r") #TODO: This is likely the most accurate way to pick a chain responsively
    role = json.loads(f.read())["role"]
    f.close()
    if role == "initiator":
        f = open(self.currentswapname + "/initiation.atomicswap", "r")
        initiatorChain = json.loads(f.read())["localChain"]
        f.close()
        if initiatorChain == "Ergo":
            f = open("SigmaParticle/" + self.currentswapname + "/boxId", "r")
            boxId = f.read()
            f.close()
            lockHeightCMD = \
                            "cd SigmaParticle/boxConstantByIndex && ./deploy.sh " + boxId + \
                            " 7 ../../" + self.currentswapname + "/localChain_lockHeight"
            devnull = open(os.devnull, 'wb')
            response = subprocess.Popen(lockHeightCMD, shell=True,
                                 stdout=devnull, stderr=devnull,
                                 close_fds=True)


            currentHeightCMD = \
                            "cd SigmaParticle/currentHeight && ./deploy.sh ../../" + \
                            self.currentswapname + "/localChain_currentHeight"

            response = subprocess.Popen(currentHeightCMD, shell=True,
                                 stdout=devnull, stderr=devnull,
                                 close_fds=True)
            if os.path.isfile(self.currentswapname + "/localChain_lockHeight") == True:
                f = open(self.currentswapname + "/localChain_lockHeight")
                lockHeight = f.read()
                f.close()
                f = open(self.currentswapname + "/localChain_currentHeight")
                currentHeight = f.read()
                f.close()
                if int(currentHeight) <= int(lockHeight):
                    return int(lockHeight) - int(currentHeight) + 1 #plus 1 because currently contract checks for GREATER THAN lock height
                else:
                    return 0
            else:
                print("cant find path:", self.currentswapname + "/localChain_lockHeight", "\n\n box not uploaded yet or invalid ")
    if role == "responder":
        f = open(self.currentswapname + "/response_commitment.atomicswap", "r")
        responderChain = json.loads(f.read())["chain"]
        f.close()
        if responderChain == "Sepolia":
            f = open(self.currentswapname + "/response_commitment.atomicswap", "r")
            addr = json.loads(f.read())["contractAddr"]
            f.close()
            cmd = \
                    "cd Atomicity/" + self.currentswapname + " && ./deploy.sh lockTime " + \
                    addr + " ../../" + self.currentswapname + "/remainingLockTime"
            print(cmd)
            devnull = open(os.devnull, 'wb')
            response = subprocess.Popen(cmd, shell=True,
                                 stdout=devnull, stderr=devnull,
                                 close_fds=True)
            if os.path.isfile(self.currentswapname + "/remainingLockTime"):
                f = open(self.currentswapname + "/remainingLockTime", "r")
                lockTime = f.read()
                f.close()
                return lockTime
            else:
                print("failed to create or find remainingLockTime file")

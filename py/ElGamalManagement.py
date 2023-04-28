import time
import os
import json
from threading import *


def dirElGamalKeysGetLast(self):
    Keys = []
    for file in self.thisDir:
        if file.endswith('.ElGamalKey'):
            f = open(file, "r")
            j = json.loads(f.read())
            self.keyDict[j["Public Key"]] = j["Private Key"]
            Keys.append(file)
    Keys.sort()
    lastkey = Keys.pop()
    f = open(lastkey, "r")
    j = json.loads(f.read())
    self.ElGamalPublicKey = j["Public Key"]
    self.ElGamalPub.configure(text="ElGamal Key File: " + lastkey)
    return lastkey
    

def firstElGamalKey(self):
    for file in self.thisDir:
        if file.endswith('.ElGamalKey'):
            f = open(file, "r")
            j = json.loads(f.read())
            self.keyDict[j["Public Key"]] = j["Private Key"]
    if len(self.keyDict) == 0: #if there are no ElGamal Keys in the dir then make a new one
        self.ElGamalPublicKey = os.popen("./ElGamal genPubKey").read().rstrip()
        f = open(self.ElGamalPublicKey, "r")
        self.ElGamalKeyFileName = "Key0.ElGamalKey"
        j = json.loads(f.read())
        self.ElGamalPublicKey = j["Public Key"]
        self.keyDict[j["Public Key"]] = j["Private Key"]
        self.ElGamalPub.configure(text="ElGamal Key File: " + self.ElGamalKeyFileName)
        return True
    else:
        return False

def genNewElGamalKey(self):
    def work():
        self.ElGamalPublicKey = os.popen("./ElGamal genPubKey").read().rstrip()
        f = open(self.ElGamalPublicKey , "r")
        self.ElGamalKeyFileName = self.ElGamalPublicKey
        j = json.loads(f.read())
        self.ElGamalPublicKey = j["Public Key"]
        self.keyDict[j["Public Key"]] = j["Private Key"]
        self.ElGamalPub.configure(text="ElGamal Key File: " + self.ElGamalKeyFileName)
    self.thread_pool_executor.submit(work)

import time
import os
import json
from threading import *


def dirElGamalKeysGetLast(self):
    for file in self.thisDir:
        if file.endswith('.ElGamalKey'):
            f = open(file, "r")
            j = json.loads(f.read())
            self.keyDict[j["Public Key"]] = j["Private Key"]
            self.ElGamalPublicKey = j["Public Key"] #uses the last public key found as default

def firstElGamalKey(self):
    if len(self.keyDict) == 0: #if there are no ElGamal Keys in the dir then make a new one
        self.ElGamalPublicKey = os.popen("./ElGamal genPubKey").read().rstrip()
        f = open(self.ElGamalPublicKey, "r")
        j = json.loads(f.read())
        self.keyDict[j["Public Key"]] = j["Private Key"]

def genNewElGamalKey(self):
    def work():
        self.ElGamalPublicKey = os.popen("./ElGamal genPubKey").read().rstrip()
        f = open(self.ElGamalPublicKey , "r")
        j = json.loads(f.read())
        self.keyDict[j["Public Key"]] = j["Private Key"]
        self.ElGamalPub.configure(text="ElGamal PubKey: " + j["Public Key"])
    self.thread_pool_executor.submit(work)

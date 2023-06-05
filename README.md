**In Development**

### THIS IS EXPERIMENTAL SOFTWARE IN EARLY STAGES OF DEVELOPMENT, <u>DO NOT USE WITH MAINNET FUNDS!!! TESTNET ONLY STAGE OF SOFTWARE</u> USE AT OWN RISK. 

# ElGamal Atomic Swap Client

**Current Project Status**:
  * Tested under Ubuntu Linux
  * Currently requires: [Custom ElGamal Client rsElgamal](https://github.com/dzyphr/rsElGamal/settings)
  * Plans to include better known encryption libraries like libsodium, or pycryptodome
  * Working Atomic Swap tested with initiator on Ergo and responder on Sepolia


**To run**:
  * Clone the repo
  * `cd` into cloned repo
  * `mkdir rust`
  * Clone [Custom ElGamal Client rsElgamal](https://github.com/dzyphr/rsElGamal/settings) into new `rust` directory
  * create a .env file for respective chain keys and rpc info:
    - For Ergo (create at `SigmaParticle/basic_framework/.env`):
        - testnetNode="http://127.0.0.1:9052/"
        - mnemonic="your mnemonic seed phrase written like this"
        - mnemonicPass="yourPasswordIfYouHaveOneIfNotLeaveBlank"
        - senderEIP3Secret=pubkeyIndex
        - apiURL="https://tn-ergo-explorer.anetabtc.io/" (or another explorer)
        
    - For EVM chains<sub>[Sepolia, Goerli]</sub> (create at `Atomicity/basic_framework/.env`)
        - SepoliaSenderAddr="0xYourAddr"
        - SepoliaPrivKey="0xyourprivatekeyhex"
        - Sepolia="chain specific rpc https:// address"
        - SepoliaID="11155111" (chain ID)
        - SepoliaScan="https://api-sepolia.etherscan.io/api" (block explorer for verification)
        
        (repeat chain specific arguments for each respective chain)
        
        - EtherscanAPIKey="YourAPIKeyForBlockExplorerVerification"
        - VerifyBlockExplorer="True" (optional, good for rescue circumstances)
        - SolidityCompilerVersion="0.8.0" (currently working with this)
        

         

  ( before continuing make sure you are in AtomicElGamalClient directory )

  * run `. venv-steps-debian.sh`

  ( if first run `chmod +x venv-steps-debian.sh` before running above cmd )





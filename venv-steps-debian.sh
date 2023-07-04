sudo apt install python3.10-venv &&
python3 -m venv . &&
chmod +x bin/activate && . bin/activate &&
python3 -m pip install python-dotenv &&
python3 -m pip install pyperclip &&
python3 -m pip install py-solc-x &&
python3 -m pip install pip install web3==5.31.3 &&
python3 -m pip install ergpy &&
python3 -m pip install numpy &&
python3 -m pip install libnum &&
python3 -m pip install customtkinter && 
python3 py/main.py &&
deactivate


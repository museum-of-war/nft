Welcome to the ERC721xyz repo!

To run this script, install brownie on terminal:

pip install eth-brownie

We only use OpenSea dependencies, install as follows on terminal:

brownie pm install OpenZeppelin/openzeppelin-contracts@4.0.0

Compile contracts:

brownie compile

Running contracts:

All logic for contract constructors and deployment with relevant comments can be found on scripts/deploy.py

To deploy contracts:

brownie run deploy
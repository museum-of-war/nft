# Welcome to the Meta History Smart Contracts repo!

To run this script, install brownie on terminal:

```
pip install eth-brownie
```

We only use OpenZeppelin dependencies, install as follows on terminal:

```
brownie pm install OpenZeppelin/openzeppelin-contracts@4.0.0
```

Compile contracts:

```
brownie compile
```

If compilation fails, empty the `build` folder (not included in the repo as part of `.gitignore`)

Running contracts:

`ganache` is the default network defined on brownie-config.yaml - edit here whichever network you want to use
from 

```
brownie networks list
``` 

or create your own using 
```
$ brownie networks add <env> <id? [key=value, ...]
```

All logic for contract constructors and deployment with relevant comments can be found on `scripts/deploy.py`

To test contracts:

```
brownie test 
```

To deploy contracts:

```
brownie run deploy
```

## Testing

https://goerlifaucet.com/  - charge your account with virtual eth for gas on Goerli testnet

## Testing SelectiveDropMHv2

Make sure that `scripts/deploy_drop.py` script has propper params
use `brownie run deploy_drop --network goerli` to deploy to the testnet

`brownie console --network goerli`
>>> `from brownie import SelectiveDropMHv2`
>>> `contract = SelectiveDropMHv2.at("0x84998969952a0d9910D581417044139847D168C7")` # with new contract deployed address
>>> `owner = accounts.load('testnet2')` # or whichever local name you have an account with
>>> `contract.airdrop(list(range(1, 51)), owner, {'from': owner}) ` // to aidrop to your account nfts, currently airdrops 50

## Docs

If you want to read more about smart contracts, you can visit the [docs](/docs)!

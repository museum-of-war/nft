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
`from brownie import SelectiveDropMHv2`
`contract = SelectiveDropMHv2.at("0x4F9553af4ddf9573FA0034d78F2a84906f8394df")` # with new contract deployed address
`owner = accounts.load('eth-account')` # or whichever local name you have an account with
`contract.airdrop(list(range(1, 51)), owner, {'from': owner})` // to aidrop to your account nfts, currently airdrops 50
Then check with public `0x41BaD15c0cD04B0587C4A562A98630921ef343C2` address of user `eth-account` your collection

## Docs

If you want to read more about smart contracts, you can visit the [docs](/docs)!


Last transaction
0x30a5a2a97eec20aa13aac67dbc74a36cbc40b126bf6a8b8d786b431be7e79255
Deployed at
0x4F9553af4ddf9573FA0034d78F2a84906f8394df

owner = accounts.load('eth-account')

airdrop transaction
0xddc2aef2f36c5b038d21dcc886fee3c9b79c4f8f8f62f932f9c5d04ca1437c2b

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

## Docs

If you want to read more about smart contracts, you can visit the [docs](/docs)!

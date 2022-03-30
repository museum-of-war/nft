# Welcome to the ERC721xyz repo!

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

`ganache-local` is the default network defined on brownie-config.yaml - edit here whichever network you want to use
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

<i> brownie test </i>

To deploy contracts:

```
brownie run deploy
```

## About ERC721xyz

ERC721xyz implements *batch minting*, this means it allows for minting of multiple NFTs for the cost of minting
a single NFT.

To do this, we define a new mapping `orig_owners`, employ some checks in the `ownerOf(uint256 tokenId)` function, so that it employs a combination of the mappings `orig_owners` and `owners` to determine the owner of a certain `tokenId`.

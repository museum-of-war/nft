<b> Welcome to the ERC721xyz repo! </b>

To run this script, install brownie on terminal:

<i> pip install eth-brownie </i>

We only use OpenSea dependencies, install as follows on terminal:

<i> brownie pm install OpenZeppelin/openzeppelin-contracts@4.0.0 </i>

Compile contracts:

<i> brownie compile </i>

If compilation fails, empty the 'build' folder (not included in the repo as part of .gitignore)

Running contracts:

All logic for contract constructors and deployment with relevant comments can be found on scripts/deploy.py

To deploy contracts:

<i> brownie run deploy </i>

**About ERC721xyz**

ERC721xyz implements _batch minting_, this means it allows for minting of multiple NFTs for the cost of minting
a single NFT.

To do this, we define a new mapping orig_owners, employ some checks in the ownerOf(uint256 tokenId) function, so that
it employs a combination of the mappings orig_owners and owners to determine the owner of a certain tokenId.

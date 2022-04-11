# [ERC721xyz](/contracts/ERC721xyz.sol) - custom ERC721 implementation (by Fair.xyz)

ERC721xyz implements *batch minting*, this means it allows for minting of multiple NFTs for the cost of minting
a single NFT.

To do this, we define a new mapping `orig_owners`, employ some checks in the `ownerOf(uint256 tokenId)` function, so that it employs a combination of the mappings `orig_owners` and `owners` to determine the owner of a certain `tokenId`.

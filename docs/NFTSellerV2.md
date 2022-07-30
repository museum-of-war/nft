# [NFTSellerV2](/contracts/NFTSellerV2.sol) - Mata History seller contract

A variant of [NFTSeller](./NFTSeller.md) seller contract with batch buying.
Can be used only for sales. Supports ERC721 and ERC1155 tokens.
If `onlyWhitelisted` is enabled, only owners of whitelisted collections (see `whitelistedPassCollections`) can buy tokens.

Copied from: https://github.com/museum-of-war/auction.

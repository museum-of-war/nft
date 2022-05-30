# [NFTSeller](/contracts/NFTSeller.sol) - Mata History seller contract

A simplified variant of [NFTAuction](./NFTAuction.md) auction contract.
Can be used only for sales.
If `onlyWhitelisted` is enabled, only owners of whitelisted collections (see `whitelistedPassCollections`) can buy tokens.
Spends less gas than the NFTAuction.

Copied from: https://github.com/museum-of-war/auction.

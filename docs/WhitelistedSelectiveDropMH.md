# [WhitelistedSelectiveDropMH](/contracts/WhitelistedSelectiveDropMH.sol) - smart contract for fourth drop (Warline continuation)

WhitelistedSelectiveDropMH contract is used for fourth drop on Meta History: Warline.
It may be also used for next drops.

This contract is based on ERC1155.
Third drop contains 100 events with 8 copies
(800 tokens total, see `tokensCount`, `maxSupply` and `getMaxTokens` in [SelectiveDropMH](./SelectiveDropMH.md)).
The minter must be in the whitelist to mint. It is also possible to set the receiver address for minted NFTs (see `mintTo`).
The minter cannot mint tokens until the `startTime`.

Also, it is possible to set the maximum number of mints per wallet (see `maxMintsPerWallet`).
If `price` = 0 and `maxMintsPerWallet` = 1 then this contract can be used for 'free mint' (1 free NFT per address from `whitelistedAddresses`).

All funds from the sale go directly to the official crypto-account of the Ministry of Digital Transformation of Ukraine (see [`ukraineAddress`](https://etherscan.io/address/0x165CD37b4C644C2921454429E7F9358d18A45e14)).
Anybody can call `withdraw` function to send ETH from contract to `ukraineAddress`.

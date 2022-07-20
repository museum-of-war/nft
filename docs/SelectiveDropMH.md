# [SelectiveDropMH](/contracts/SelectiveDropMH.sol) - smart contract for third drop (Warline continuation)

SelectiveDropMH contract is used for third drop on Meta History: Warline.
It may be also used for all next drops.

This contract is based on ERC1155.
Third drop contains 100 events with 12 copies
(1200 tokens total, see `tokensCount`, `maxSupply` and `getMaxTokens`).
The minter can select token ids to mint. It is also possible to set the receiver address for minted NFTs (see `mintTo`).

Also, it is possible to set the maximum number of mints per wallet (see `maxMintsPerWallet`).

All funds from the sale go directly to the official crypto-account of the Ministry of Digital Transformation of Ukraine (see [`ukraineAddress`](https://etherscan.io/address/0x165CD37b4C644C2921454429E7F9358d18A45e14)).
Anybody can call `withdraw` function to send ETH from contract to `ukraineAddress`.

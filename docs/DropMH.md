# [DropMH](/contracts/DropMH.sol) - smart contract for second drop (Warline continuation)

DropMH contract is used for second drop on Meta History: Warline.
It may be also used for all next drops.  

This contract is based on ERC1155.
Second drop contains 100 events with 16 copies
(1600 tokens total, see `tokensCount`, `maxSupply` and `getMaxTokens`). 
Also, now it is possible to add `burner` address (see `setBurner`) - a smart-contract that will be used for merging.
As in the first drop, elements are minted "in cycles": 1, 2, 3, ..., 100, 1, 2, ..., 100 and so on.

Also, it is possible to set the maximum number of mints per wallet (see `maxMintsPerWallet`).

All funds from the sale go directly to the official crypto-account of the Ministry of Digital Transformation of Ukraine (see [`ukraineAddress`](https://etherscan.io/address/0x165CD37b4C644C2921454429E7F9358d18A45e14)).
Anybody can call `withdraw` function to send ETH from contract to `ukraineAddress`.

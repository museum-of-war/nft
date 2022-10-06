# [SelectiveDropMHv2](/contracts/SelectiveDropMHv2.sol) - smart contract for fifth drop (Warline continuation)

SelectiveDropMH contract is used for fifth drop on Meta History: Warline.
It may be also used for next drops.

This contract is based on ERC1155.
Fifth drop contains 100 events with 4 copies
(400 tokens total, see `tokensCount`, `maxSupply` and `getMaxTokens`).
The minter can select token ids to mint. It is also possible to set the receiver address for minted NFTs (see `mintTo`).
The minter cannot mint tokens until the `startTime`.

Also, it is possible to set the maximum number of mints per wallet (see `maxMintsPerWallet`).

All funds from the sale go directly to the withdraw address, which can be set on deploy (see `withdrawAddress` and `withdrawAddress_` in constructor).
Anybody can call `withdraw` function to send ETH from contract to `withdrawAddress`.

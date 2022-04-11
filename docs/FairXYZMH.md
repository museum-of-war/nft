# [FairXYZMH](/contracts/FairXYZMH.sol) - Meta History first drop contract (by Fair.xyz)

FairXYZMH contract is used for first drop on Meta History: Warline.

## Collection

This collection contains 4 unique tokens and 99 elements with 22 editions (2182 tokens total).
Non-unique elements go "in cycles": 1, 2, 3, ..., 99, 1, 2, ..., 99 and so on.
So tokens #5, #104 (5 + 99), ..., #2084 (5 + 99 * 21) represent the same element but have different 'editions'.
These elements represent first 103 events on [Warline](https://metahistory.gallery/warline).
First four tokens are unique (
[1](https://opensea.io/assets/0xd3228e099e6596988ae0b73eaa62591c875e5693/1),
[2](https://opensea.io/assets/0xd3228e099e6596988ae0b73eaa62591c875e5693/2),
[3](https://opensea.io/assets/0xd3228e099e6596988ae0b73eaa62591c875e5693/3),
[4](https://opensea.io/assets/0xd3228e099e6596988ae0b73eaa62591c875e5693/4)
), so they represent first four events.
For events from 5 to 103 tokenId is calculated by formula:
`tokenId = eventId + 99 * (editionNumber - 1)`

Examples:
- token ID for the first edition of event #103 will be equal to [103](https://opensea.io/assets/0xd3228e099e6596988ae0b73eaa62591c875e5693/103);
- token ID for the second edition of event #5 will be equal to [104](https://opensea.io/assets/0xd3228e099e6596988ae0b73eaa62591c875e5693/104);
- token ID for the third edition of event #50 will be equal to [248](https://opensea.io/assets/0xd3228e099e6596988ae0b73eaa62591c875e5693/248);
- token ID for the 22nd edition of event #103 will be equal to [2182](https://opensea.io/assets/0xd3228e099e6596988ae0b73eaa62591c875e5693/2182).

Only signed messages by Fair.xyz minting system can be used to mint tokens
(see `signature` of `mint` function in [FairXYZMH.sol](/contracts/FairXYZMH.sol),
`test_mint` in [meta_history_test.py](/tests/meta_history_test.py)
and [FairXYZWallets](./FairXYZWallets.md)).

Also, it is possible to set the maximum number of mints per wallet (see `Max_mints_per_wallet`).

All funds from the sale go directly to the official crypto-account of the Ministry of Digital Transformation of Ukraine (see [`ukraineAddress`](https://etherscan.io/address/0x165CD37b4C644C2921454429E7F9358d18A45e14)).
Anybody can call `withdraw` function to send ETH from contract to `ukraineAddress`.

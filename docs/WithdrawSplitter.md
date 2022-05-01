# [WithdrawSplitter](/contracts/WithdrawSplitter.sol) - smart contract to withdraw ETH to Ukraine and one other address according to proportions

This contract is used to send ETH to 
the official crypto-account of the Ministry of Digital Transformation of Ukraine (see [`ukraineAddress`](https://etherscan.io/address/0x165CD37b4C644C2921454429E7F9358d18A45e14))
and one other address according to the given proportions.
It can be used to send ETH to the artists' shared wallet.

Proportions and addresses are immutable.

Anybody can call `withdraw` function - the amount of ETH will be divided according to the proportions
and will be sent to the `ukraineAddress` and `otherAddress`.

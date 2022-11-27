# [WithdrawSplitterV2](/contracts/WithdrawSplitterV2.sol) - smart contract to withdraw ETH to the specified addresses according to proportions

This contract is used to divide/split ETH before sending to 
multiple wallets according to the given proportions.
It can be used to send ETH to the artists' wallet and collect fees.

Proportions and addresses cannot be changed.

Anybody can call `withdraw` function - the amount of ETH will be divided according to the proportions
and will be sent to the addresses of receivers that can be set up via constructor.

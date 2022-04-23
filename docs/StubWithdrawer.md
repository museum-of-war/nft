# [StubWithdrawer](/contracts/StubWithdrawer.sol) - smart contract to withdraw locked ETH

This contract is used to recover ETH that were sent in the wrong network.
For example, if we find address of our contract in different chains with locked ETH,
we can deploy this contract and send all ETH to the owners.
This contract will also prevent new transactions (see `revert` in `fallback` and `receive`). 

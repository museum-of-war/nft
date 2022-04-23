// SPDX-License-Identifier: MIT

pragma solidity 0.8.13;

import "OpenZeppelin/openzeppelin-contracts@4.0.0//contracts/access/Ownable.sol";

contract StubWithdrawer is Ownable {
    string public message = "Ethereum Mainnet";

    constructor(string memory message_) {
        message = message_;
    }

    function withdraw(address[] memory addresses, uint256 amount) external onlyOwner
    {
        for (uint i = 0; i < addresses.length; i++) payable(addresses[i]).transfer(amount);
    }

    fallback() external payable {
        revert(message);
    }

    receive() external payable {
        revert(message);
    }
}

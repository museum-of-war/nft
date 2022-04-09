// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

interface ISimpleMinter {
    function mint(address to) external returns (uint256);
}

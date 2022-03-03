// SPDX-License-Identifier: MIT

pragma solidity 0.8.4;

import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";


abstract contract SafeUpgradable is UUPSUpgradeable {

    modifier onlyOwner {
        require(msg.sender == _getAdmin(), "Access denied");
        _;
    }

    function init(address owner) public initializer {
        _changeAdmin(owner);
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner view {}
}

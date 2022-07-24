// SPDX-License-Identifier: MIT

pragma solidity 0.8.15;

import "./SelectiveDropMH.sol";

contract WhitelistedSelectiveDropMH is SelectiveDropMH {
    bool internal isLockedWhitelist;
    mapping(address => bool) public whitelistedAddresses;

    constructor(uint256 price_, uint256 tokensCount_, uint256 maxSupply_, string memory name_, string memory symbol_,
                uint256 maxMintsPerWallet_, string memory baseURI_, uint256 startTime_, address[] memory whitelisted_)
                SelectiveDropMH(price_, tokensCount_, maxSupply_, name_, symbol_, maxMintsPerWallet_, baseURI_, startTime_) {
        for (uint256 i = 0; i < whitelisted_.length; i++) whitelistedAddresses[whitelisted_[i]] = true;
    }

    // Lock whitelist forever
    function lockWhitelist() external onlyOwner {
        isLockedWhitelist = true;
    }

    // Add addresses to whitelist
    function addWhitelistedAddresses(address[] memory whitelisted_) external onlyOwner {
        require(!isLockedWhitelist, "Whitelist change has been locked");
        for (uint256 i = 0; i < whitelisted_.length; i++) whitelistedAddresses[whitelisted_[i]] = true;
    }

    // Remove addresses from whitelist
    function removeWhitelistedAddresses(address[] memory whitelisted_) external onlyOwner {
        require(!isLockedWhitelist, "Whitelist change has been locked");
        for (uint256 i = 0; i < whitelisted_.length; i++) delete whitelistedAddresses[whitelisted_[i]];
    }

    // Mint tokens to address
    function mintTo(uint256[] memory tokenIds, address to) payable public override {
        require(whitelistedAddresses[to] == true, "The recipient is not whitelisted!");

        super.mintTo(tokenIds, to);
    }
}

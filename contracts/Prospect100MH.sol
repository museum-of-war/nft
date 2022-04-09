// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

import 'OpenZeppelin/openzeppelin-contracts@4.0.0//contracts/token/ERC721/ERC721.sol';
import "OpenZeppelin/openzeppelin-contracts@4.0.0//contracts/access/Ownable.sol";
import "./interfaces/ISimpleMinter.sol";

contract Prospect100MH is ERC721, Ownable, ISimpleMinter {
    string internal baseURI;
    bool internal isLockedURI;

    uint256 public nextTokenId;

    address public minterAddress;

    constructor(string memory name_, string memory symbol_,
        string memory baseURI_, uint256 instantAirdrop) payable ERC721(name_, symbol_) {
        baseURI = baseURI_;
        for (uint256 i = 1; i <= instantAirdrop; i++) _mint(msg.sender, i);
        nextTokenId = instantAirdrop + 1;
    }

    modifier onlyMinter() {
        require(msg.sender == minterAddress, "Not a minter");
        _;
    }

    function changeMinterAddress(address minterAddress_) external onlyOwner {
        minterAddress = minterAddress_;
    }

    // lock metadata forever
    function lockURI() external onlyOwner {
        isLockedURI = true;
    }

    // modify the base URI
    function changeBaseURI(string memory newBaseURI) onlyOwner external
    {
        require(!isLockedURI, "URI change has been locked");
        baseURI = newBaseURI;
    }

    // return Base URI
    function _baseURI() internal view override returns (string memory) {
        return baseURI;
    }

    //only minter - mints next token to address
    function mint(address to) external onlyMinter override returns (uint256) {
        uint256 tokenId = nextTokenId;
        _mint(to, tokenId);
        nextTokenId++;
        return tokenId;
    }
}

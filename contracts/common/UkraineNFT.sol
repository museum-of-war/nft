// SPDX-License-Identifier: MIT

pragma solidity 0.8.4;

// import "../abstract/SafeUpgradable.sol";

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/interfaces/IERC2981.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";


contract UkraineNFT is Ownable, ERC721, IERC2981 {
    using Strings for uint;

    string[] urls;
    uint[] indexes;
    uint nextId;

    uint public price;
    address public charityAddress;

    constructor(
        string memory _name,
        string memory _symbol,
        uint _price,
        address _charityAddress
    ) ERC721(_name, _symbol) {
        price = _price;
        charityAddress = _charityAddress;
    }

    function totalSupply() public view returns (uint256) {
        return indexes.length == 0 ? 0 : indexes[indexes.length - 1];
    }

    function prepareBatch(string memory url, uint count) external onlyOwner {
        urls.push(url);
        indexes.push(totalSupply() + count);
    }

    function changeCharityAddress(address newCharityAddress) external onlyOwner {
        charityAddress = newCharityAddress;
    }

    function changePrice(uint newPrice) external onlyOwner {
        price = newPrice;
    }

    function mint() external payable returns (uint tokenId) {
        require(nextId < totalSupply(), "ERC721: minting nonexistent token");
        require(msg.value >= price, "Not enough ETH");
        tokenId = nextId;
        _safeMint(msg.sender, tokenId);
        nextId++;

        (bool success, ) = payable(charityAddress).call{value: msg.value}("");
        require(success, "Failed to send Ether to charity address");
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");

        uint index;
        for(uint i = 0; i < indexes.length; i++) {
            if (tokenId < indexes[i]) {
                index = i;
                break;
            }
        }

        string memory baseURI = urls[index];
        return string(abi.encodePacked(baseURI, tokenId.toString()));
    }

    function royaltyInfo(uint256, uint256 salePrice)
    external
    view
    override
    returns (address receiver, uint256 royaltyAmount) {
        receiver = owner();
        royaltyAmount = salePrice / 10; //10%
    }
}

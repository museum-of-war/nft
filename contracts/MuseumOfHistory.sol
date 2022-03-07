// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

import "@openzeppelin/contracts-upgradeable/token/ERC721/ERC721Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/interfaces/IERC2981Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";


contract MuseumOfHistory is Initializable, IERC2981Upgradeable, ERC721Upgradeable, OwnableUpgradeable, UUPSUpgradeable {
    
    using Strings for uint;

    string[] urls;
    uint[] indexes;

    uint public nextId;
    uint public price;
    uint public priceStep;
    uint public priceIncreaseIdStep;
    uint public nextPriceIncreaseId;

    address public charityAddress;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() initializer {}

    function initialize(
        uint initialPrice, // 0.1 ether
        uint initialPriceIncreaseIdStep, // 50
        uint initialPriceStep, // 0.02 ether
        address initialCharityAddress // 0x165CD37b4C644C2921454429E7F9358d18A45e14
    ) initializer public {
        __ERC721_init("Museum of History", "MOH");
        __Ownable_init();
        __UUPSUpgradeable_init();

        price = initialPrice;
        priceIncreaseIdStep = initialPriceIncreaseIdStep;
        nextPriceIncreaseId = priceIncreaseIdStep;
        priceStep = initialPriceStep;
        charityAddress = initialCharityAddress;
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

    function mint() external payable returns (uint tokenId) {
        require(nextId < totalSupply(), "ERC721: minting nonexistent token");
        require(msg.value >= price, "Not enough ETH");
        
        tokenId = nextId;
        _safeMint(msg.sender, tokenId);

        nextId++;
        if (nextId == nextPriceIncreaseId) {
            nextPriceIncreaseId += priceIncreaseIdStep;
            price += priceStep;
        }

        (bool success, ) = payable(charityAddress).call{value: msg.value}("");
        require(success, "Failed to send Ether to charity address");
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(tokenId < totalSupply(), "ERC721Metadata: URI query for nonexistent token");

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

    function getIntervals() external view returns (string[] memory baseURIs, uint[] memory endsOfIntervals) {
        uint count = indexes.length;
        baseURIs = new string[](count);
        endsOfIntervals = new uint[](count);
        for (uint i = 0; i < count; i++) {
            baseURIs[i] = urls[i];
            endsOfIntervals[i] = indexes[i];
        }
    }

    receive() external payable { }

    fallback() external payable { }

    function royaltyInfo(uint256, uint256 salePrice)
    external
    view
    override
    returns (address receiver, uint256 royaltyAmount) {
        receiver = address(this);
        royaltyAmount = salePrice * 8 / 10; //80%
    }

    function withdrawEther() external {
        uint amount = address(this).balance; // 80% of sale price

        uint ownerWithdraw = amount / 8; // 10% of sale price
        uint charityWithdraw = ownerWithdraw * 7; // 70% of sale price

        (bool success1, ) = payable(owner()).call{value: ownerWithdraw}("");
        (bool success2, ) = payable(charityAddress).call{value: charityWithdraw}("");
        require(success1 && success2, "Failed to send Ether");
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        onlyOwner
        override
    {}
}

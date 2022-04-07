// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

import 'OpenZeppelin/openzeppelin-contracts@4.0.0//contracts/token/ERC721/IERC721.sol';
import 'OpenZeppelin/openzeppelin-contracts@4.0.0//contracts/token/ERC721/ERC721.sol';
import "OpenZeppelin/openzeppelin-contracts@4.0.0//contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0//contracts/security/ReentrancyGuard.sol";

contract MergerMH is ERC721, Ownable, ReentrancyGuard {
    address public constant burnAddress = address(0x000000000000000000000000000000000000dEaD);

    string internal baseURI;
    bool internal isLockedURI;

    address public immutable nftAddress;
    // NFTs from 'offset + 1' to 'offset + elementsCount * editionsCount' can be merged
    uint16 internal immutable offset; //NFTs that don't take part in merging
    uint16 internal immutable elementsCount;
    uint16 internal immutable editionsCount;
    uint16[] internal /*immutable*/ startTokenIds;
    uint16[][] internal nextTokenIds;

    constructor(string memory name_, string memory symbol_,
                address nftAddress_, string memory URI_base,
                uint16 offset_, uint16 elementsCount_, uint16 editionsCount_) payable ERC721(name_, symbol_) {
        nftAddress = nftAddress_;
        baseURI = URI_base;
        offset = offset_;
        elementsCount = elementsCount_;
        editionsCount = editionsCount_;

        uint16 totalMergesCount = editionsCount_ - 1; // 16 editions gives 8 + 4 + 2 + 1 = (16 - 1) merges (complete binary tree nodes count)
        require(totalMergesCount * elementsCount_ <= type(uint16).max, "Too many elements");

        uint16 startId = 1; // start, so must add 1
        startTokenIds.push(startId);
        for (uint16 mergesCount = editionsCount_ / 2; mergesCount > 0; mergesCount /= 2) {
            startId += mergesCount; // if 16 editions, then: +8, +4, +2, +1
            startTokenIds.push(startId);
        }

        uint256 levelsCount = startTokenIds.length;

        for (uint16 i = 0; i < elementsCount_; i++) {
            uint16[] memory nextIds = new uint16[](levelsCount);
            uint16 elementOffset = i * totalMergesCount;
            for (uint16 j = 0; j < levelsCount; j++) nextIds[j] = elementOffset + startTokenIds[j];
            nextTokenIds.push(nextIds);
        }
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

    // merge 2 NFTs into one (from other contract - nftAddress)
    function mergeBase(uint256 tokenId1, uint256 tokenId2) external nonReentrant returns (uint256) {
        require(msg.sender == tx.origin, "Sender must be a wallet");
        require(tokenId1 > offset && tokenId2 > offset, "Cannot merge unique token");
        require(tokenId1 != tokenId2, "Cannot merge token with self");

        int difference = int(tokenId2) - int(tokenId1);

        int periodsCount = difference / int16(elementsCount); // elements go in cycles: 1, 2, ... 99, 1, 2, ... 99, ...

        uint256 restoredTokenId2 = uint256(periodsCount * int16(elementsCount) + int(tokenId1));
        require(restoredTokenId2 == tokenId2, "Cannot merge different elements");

        //tokenId = offset + elementsCount * editionIndex + elementId, so:
        uint256 elementId = (tokenId1 - offset) % elementsCount;

        uint256 mintingTokenId = nextTokenIds[elementId - 1][0];

        IERC721 nftContract = IERC721(nftAddress);
        // burning
        nftContract.transferFrom(msg.sender, burnAddress, tokenId1);
        nftContract.transferFrom(msg.sender, burnAddress, tokenId2);

        _mint(msg.sender, mintingTokenId);

        nextTokenIds[elementId - 1][0]++;
        return mintingTokenId;
    }

    // merge 2 NFTs with n level into one with n+1 level (from this contract)
    function mergeAdvanced(uint256 tokenId1, uint256 tokenId2) external nonReentrant returns (uint256) {
        require(msg.sender == tx.origin, "Sender must be a wallet");
        require(msg.sender == ownerOf(tokenId1) && msg.sender == ownerOf(tokenId2), "Sender must be an owner");
        require(tokenId1 != tokenId2, "Cannot merge token with self");

        uint256 maxDistance = editionsCount / 2; // for 16 editions it can only be 8 merged elements with 1st level
        int distance = int(tokenId2) - int(tokenId1);
        uint256 absDistance = distance > 0 ? uint256(distance) : uint256(-distance);
        require(absDistance < maxDistance, "Cannot merge different tokens");

        uint256 totalMergesCount = editionsCount - 1; // explained in constructor

        for (uint256 elementIndex = 0; elementIndex < startTokenIds.length; elementIndex++) {
            uint256 elementOffset = elementIndex * totalMergesCount;
            uint256 firstId = elementOffset + startTokenIds[0];
            // tokens must belong to [firstId, firstId + totalMergesCount) interval
            if (tokenId1 < firstId || tokenId1 >= firstId + totalMergesCount) continue;
            require(tokenId2 >= firstId && tokenId2 < firstId + totalMergesCount, "Cannot merge different tokens");

            uint256 lastIndex = startTokenIds.length - 2; // skip last level - it cannot be merged
            for (uint256 level = 0; level <= lastIndex; level++) {
                uint256 nextLevel = level + 1;
                uint256 currentLevelId = elementOffset + startTokenIds[level];
                uint256 nextLevelId = elementOffset + startTokenIds[nextLevel];
                // tokens must belong to [currentLevelId, nextLevelId) interval
                if (tokenId1 < currentLevelId || tokenId1 >= nextLevelId) continue;
                require(tokenId2 >= currentLevelId && tokenId2 < nextLevelId, "Cannot merge different tokens");

                // burning
                _burn(tokenId1);
                _burn(tokenId2);

                uint256 mintingTokenId = nextTokenIds[elementIndex][nextLevel];
                _mint(msg.sender, mintingTokenId);

                //TODO: merge reward for high levels

                nextTokenIds[elementIndex][nextLevel]++;
                return mintingTokenId;
            }
        }
        revert("ERROR"); // something went wrong
    }
}

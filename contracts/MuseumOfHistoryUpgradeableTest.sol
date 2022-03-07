// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

import "./MuseumOfHistory.sol";

contract MuseumOfHistoryUpgradeableTest is MuseumOfHistory { // only for test purposes
    function changePriceIncreaseIdStep(uint newPriceIncreaseIdStep) external onlyOwner {
        nextPriceIncreaseId = nextPriceIncreaseId + newPriceIncreaseIdStep - priceIncreaseIdStep;
        priceIncreaseIdStep = newPriceIncreaseIdStep;

        while (nextId >= nextPriceIncreaseId) {
            nextPriceIncreaseId += priceIncreaseIdStep;
            price += priceStep;
        }
    }
}

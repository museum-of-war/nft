import { expect } from "chai";
import { ethers, upgrades } from "hardhat";

import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";
import {
  MuseumOfHistory,
  MuseumOfHistory__factory,
  MuseumOfHistoryUpgradeableTest,
  MuseumOfHistoryUpgradeableTest__factory,
} from "../typechain";
import {BigNumber, constants} from "ethers";

describe("Upgradable NFT controlled through UUPS Proxy", function () {
  const initialPrice = constants.WeiPerEther.div(10); // 0.1 ether
  const initialPriceIncreaseIdStep = 50;
  const initialPriceStep = constants.WeiPerEther.div(50);  // 0.02 ether
  const initialCharityAddress = "0x165CD37b4C644C2921454429E7F9358d18A45e14";
  let owner: SignerWithAddress, other: SignerWithAddress, charityMock: SignerWithAddress;
  let NFT: MuseumOfHistory;
  let ProxyAddress: string;
  let ProxyWithOtherSigner: MuseumOfHistory;
  const batchesInfo = [
    {
      url: "https://url1/",
      count: 5,
    },
    {
      url: "https://url2/",
      count: 5,
    },
    {
      url: "https://url_last/",
      count: 100,
    }
  ];

  before("Deploy NFT proxied using UUPS Proxy", async () => {
    [owner, other, charityMock] = await ethers.getSigners();
    const Factory = new MuseumOfHistory__factory(owner);

    NFT = await upgrades.deployProxy(Factory,
        [initialPrice, initialPriceIncreaseIdStep, initialPriceStep, initialCharityAddress],
        { kind: "uups" }
    ) as MuseumOfHistory;
    ProxyAddress = NFT.address;
    ProxyWithOtherSigner = NFT.connect(other);
  });

  it("Must be initialized", async () => {
    expect(await NFT.price()).to.be.equal(initialPrice);
    expect(await NFT.priceIncreaseIdStep()).to.be.equal(initialPriceIncreaseIdStep);
    expect(await NFT.priceStep()).to.be.equal(initialPriceStep);
    expect(await NFT.charityAddress()).to.be.equal(initialCharityAddress);

    expect(await NFT.nextPriceIncreaseId()).to.be.equal(initialPriceIncreaseIdStep);
  });

  it("Only owner is allowed to upgrade. Proxy address not changed after upgrade", async () => {
    const FactoryV2WrongOwner = new MuseumOfHistoryUpgradeableTest__factory(other);
    expect(
        upgrades.upgradeProxy(NFT, FactoryV2WrongOwner, { kind: "uups" })
    ).to.be.revertedWith("Access denied");

    const FactoryV2 = new MuseumOfHistoryUpgradeableTest__factory(owner);
    const ProxyV2 = await upgrades.upgradeProxy(NFT, FactoryV2, {
      kind: "uups",
    }) as MuseumOfHistoryUpgradeableTest;

    expect(ProxyV2.address).to.equal(ProxyAddress);

    NFT = ProxyV2;
  });

  it("Must support features of implementation it had upgraded to", async () => {
    const ProxyV2 = MuseumOfHistoryUpgradeableTest__factory.connect(ProxyAddress, owner);

    const newChangePriceIncreaseIdStep = 5;

    await ProxyV2.changePriceIncreaseIdStep(newChangePriceIncreaseIdStep);

    const changedPriceIncreaseIdStep = await ProxyV2.priceIncreaseIdStep();

    expect(changedPriceIncreaseIdStep.toNumber()).to.equal(newChangePriceIncreaseIdStep);
  });

   it("Must support charity address changing", async () => {
     await NFT.changeCharityAddress(charityMock.address);
     const changedAddress = await NFT.charityAddress();
     expect(changedAddress).to.be.equal(charityMock.address);
   });

   it("Only owner is allowed to change charity address", async () => {
     const transaction = ProxyWithOtherSigner.changeCharityAddress(charityMock.address);
     await expect(transaction).to.be.revertedWith("Ownable: caller is not the owner");
   });

  it("Must have zero supply and no ids on initialized", async () => {
    const supply = await NFT.totalSupply();
    expect(supply.toNumber()).to.be.equal(0);

    const tokenURITransaction = NFT.tokenURI(0);
    await expect(tokenURITransaction).to.be.revertedWith("ERC721Metadata: URI query for nonexistent token");

    const { baseURIs, endsOfIntervals } = await NFT.getIntervals();
    expect(baseURIs).to.be.empty;
    expect(endsOfIntervals).to.be.empty;

    const mintTransaction = NFT.mintNext();
    await expect(mintTransaction).to.be.revertedWith("ERC721: minting nonexistent token");
  });

   it("Must support adding new batches", async () => {
     let supply = (await NFT.totalSupply()).toNumber();

     for (const { url, count } of batchesInfo) {
       await NFT.prepareBatch(url, count);
       const newSupply = (await NFT.totalSupply()).toNumber();
       const supplyDelta = newSupply - supply;
       supply = newSupply;

       expect(supplyDelta).to.be.equal(count);
     }
   });

  it("Only owner is allowed to add new batch", async () => {
    const transaction = ProxyWithOtherSigner.prepareBatch("https://url3/", 10);
    await expect(transaction).to.be.revertedWith("Ownable: caller is not the owner");
  });

   it("Must return tokenURI for unminted tokens", async () => {
     const supply = await NFT.totalSupply();
     expect(supply.toNumber()).to.be.greaterThan(0);

     const tokenURI = await NFT.tokenURI(0);
     await expect(tokenURI).to.be.not.empty;

     const { baseURIs, endsOfIntervals } = await NFT.getIntervals();
     expect(baseURIs.length).to.be.equal(endsOfIntervals.length);
     expect(endsOfIntervals[endsOfIntervals.length - 1]).to.be.equal(supply);
   });

   it("Must not return tokenURI for nonexistent tokens", async () => {
     const supply = await NFT.totalSupply();

     const transaction = NFT.tokenURI(supply.add(1));
     await expect(transaction).to.be.revertedWith("ERC721Metadata: URI query for nonexistent token");
   });

   it("Must not mint token without ETH", async () => {
     const transaction = ProxyWithOtherSigner.mintNext();
     await expect(transaction).to.be.revertedWith("Not enough ETH");
   });

   it("Must mint next token with correct amount of ETH", async () => {
     const value = await ProxyWithOtherSigner.price();

     const transaction = ProxyWithOtherSigner.mintNext({ value });
     await expect(transaction).to.emit(NFT, "Transfer").withArgs(constants.AddressZero, other.address, 0);

     const balance = (await ProxyWithOtherSigner.balanceOf(other.address)).toNumber();
     expect(balance).to.be.equal(1);

     const tokenOwner = await ProxyWithOtherSigner.ownerOf(0);
     expect(tokenOwner).to.be.equal(other.address);
   });

   it("Must mint next token by tokenId with correct amount of ETH", async () => {
     const nextId = await ProxyWithOtherSigner.nextId();
     const value = await ProxyWithOtherSigner.price();

     const transaction = ProxyWithOtherSigner.mint(nextId, { value });
     await expect(transaction).to.emit(NFT, "Transfer").withArgs(constants.AddressZero, other.address, nextId);

     const tokenOwner = await ProxyWithOtherSigner.ownerOf(nextId);
     expect(tokenOwner).to.be.equal(other.address);
   });

   it("Must not mint token with wrong tokenId", async () => {
     const nextId = await ProxyWithOtherSigner.nextId();
     const value = await ProxyWithOtherSigner.price();

     const transactionPrev = ProxyWithOtherSigner.mint(nextId.sub(1), { value });
     await expect(transactionPrev).to.be.revertedWith("ERC721: wrong tokenId to mint");

     const transactionNext = ProxyWithOtherSigner.mint(nextId.add(1), { value });
     await expect(transactionNext).to.be.revertedWith("ERC721: wrong tokenId to mint");
   });

   it("Must return correct tokenURI for minted token", async () => {
     const tokenId = 0;
     const tokenURI = await ProxyWithOtherSigner.tokenURI(tokenId);

     expect(tokenURI).to.be.equal(batchesInfo[0].url + tokenId);
   });

   it("Must get tokens of owner", async () => {
     const tokens = await NFT.getTokensOfOwner(other.address);

     expect(tokens.length).to.be.equal(2);
     expect(tokens).to.include.deep.members([BigNumber.from(0), BigNumber.from(1)]);

     const noTokens = await NFT.getTokensOfOwner(owner.address);
     expect(noTokens).to.be.empty;
   });

   it("Must get intervals for tokens", async () => {
     const { baseURIs, endsOfIntervals } = await NFT.getIntervals();
     expect(endsOfIntervals.length).to.be.equal(baseURIs.length);

     const intervalsCount = baseURIs.length;

     const supply = await NFT.totalSupply();
     const end = endsOfIntervals[intervalsCount - 1];
     expect(end).to.be.equal(supply);

     let tokenId = 0;
     for (let i = 0; i < intervalsCount; i++) {
       const baseURI = baseURIs[i];
       const endOfInterval = endsOfIntervals[i].toNumber();

       for (; tokenId < endOfInterval; tokenId++) {
         const tokenURI = await ProxyWithOtherSigner.tokenURI(tokenId);
         expect(tokenURI).to.be.equal(baseURI + tokenId);
       }
     }
     expect(tokenId).to.be.equal(supply);
   });

  it("Must send all ETH to charity address on minted", async () => {
    const prevBalance = await charityMock.getBalance();

    const value = await ProxyWithOtherSigner.price();

    await ProxyWithOtherSigner.mintNext({ value });

    const newBalance = await charityMock.getBalance();

    const delta = newBalance.sub(prevBalance);
    expect(delta).to.be.equal(value);
  });

  it("Must get royaltyInfo and withdraw ETH", async () => {
    const salePrice = (await ProxyWithOtherSigner.price()).mul(10);
    const { receiver, royaltyAmount } = await ProxyWithOtherSigner.royaltyInfo(0, salePrice);

    expect(receiver).to.be.equal(NFT.address);
    expect(royaltyAmount).to.be.equal(salePrice.div(10).mul(8)); // 80%

    await other.sendTransaction({
      to: receiver,
      value: royaltyAmount,
    });

    const ownerPrevBalance = await owner.getBalance();
    const charityPrevBalance = await charityMock.getBalance();

    const transaction = await NFT.withdrawEther();
    const receipt = await transaction.wait();
    const gasFee = receipt.cumulativeGasUsed.mul(receipt.effectiveGasPrice);

    const ownerNewBalance = await owner.getBalance();
    const charityNewBalance = await charityMock.getBalance();

    const ownerDelta = ownerNewBalance.sub(ownerPrevBalance);
    const charityDelta = charityNewBalance.sub(charityPrevBalance);

    expect(ownerDelta).to.be.equal(salePrice.div(10).sub(gasFee)); // 10% of sale price minus gas fee
    expect(charityDelta).to.be.equal(salePrice.div(10).mul(7)); // 70% of sale price
  });

  it("Must increment price after increase step", async () => {
    const nextPriceIncreaseId = await ProxyWithOtherSigner.nextPriceIncreaseId();

    const value = await ProxyWithOtherSigner.price();

    let mintedCount = (await ProxyWithOtherSigner.nextId()).toNumber();

    for (mintedCount; mintedCount < nextPriceIncreaseId.toNumber(); mintedCount++){
      await ProxyWithOtherSigner.mintNext({ value });
    }

    const newNextPriceIncreaseId = await ProxyWithOtherSigner.nextPriceIncreaseId();
    const newValue = await ProxyWithOtherSigner.price();

    const priceIncreaseIdStep = await ProxyWithOtherSigner.priceIncreaseIdStep();
    const priceStep = await ProxyWithOtherSigner.priceStep();

    expect(newNextPriceIncreaseId).to.be.equal(nextPriceIncreaseId.add(priceIncreaseIdStep));
    expect(newValue).to.be.equal(value.add(priceStep));
  });
});

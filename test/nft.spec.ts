import { expect } from "chai";
import { ethers, upgrades } from "hardhat";

import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";
import { MuseumOfHistory, MuseumOfHistory__factory } from "../typechain";
import { constants } from "ethers";

describe("Upgradable NFT controlled through UUPS Proxy", function () {
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
    }
  ];
  let mintedCount = 0;

  before("Deploy NFT proxied using UUPS Proxy", async () => {
    [owner, other, charityMock] = await ethers.getSigners();
    const Factory = new MuseumOfHistory__factory(owner);

    NFT = await upgrades.deployProxy(Factory, [], {
      kind: "uups",
    }) as MuseumOfHistory;
    ProxyAddress = NFT.address;
    ProxyWithOtherSigner = NFT.connect(other);
  });

//   it("Only owner is allowed to call", async () => {
//     // todo
//   });

//   it("Only owner is allowed to upgrade. Proxy address not changed after upgrade", async () => {
//     const FactoryV2WrongOwner = new NFTV2__factory(other);

//     expect(
//       upgrades.upgradeProxy(Proxy, FactoryV2WrongOwner, { kind: "uups" })
//     ).to.be.revertedWith("Access denied");
//     const FactoryV2 = new NFTV2__factory(owner);
//     const ProxyV2 = await upgrades.upgradeProxy(Proxy, FactoryV2, {
//       kind: "uups",
//     });
//     expect(ProxyV2.address).to.equal(ProxyAddress);
//     Proxy = ProxyV2;
//   });

//   it("Must support features of implementation it had upgraded to", async () => {
//     // test that Proxy supports v2 functionality
//     const ProxyV2 = NFTV2__factory.connect(ProxyAddress, owner);
//     expect((await ProxyV2.val()).toNumber()).to.equal(0);
//   });

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

    const { baseURIs, endsOfIntervals } = await NFT.getMintedIntervals();
    expect(baseURIs).to.be.empty;
    expect(endsOfIntervals).to.be.empty;

    const mintTransaction = NFT.mint();
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

   it("Must not return tokenURI for unminted tokens", async () => {
     const supply = (await NFT.totalSupply()).toNumber();
     expect(supply).to.be.greaterThan(0);

     const transaction = NFT.tokenURI(0);
     await expect(transaction).to.be.revertedWith("ERC721Metadata: URI query for nonexistent token");

     const { baseURIs, endsOfIntervals } = await NFT.getMintedIntervals();
     expect(baseURIs).to.be.empty;
     expect(endsOfIntervals).to.be.empty;
   });

   it("Must not mint token without ETH", async () => {
     const transaction = ProxyWithOtherSigner.mint();
     await expect(transaction).to.be.revertedWith("Not enough ETH");
   });

   it("Must mint token with correct amount of ETH", async () => {
     const value = await ProxyWithOtherSigner.price();

     const transaction = ProxyWithOtherSigner.mint({ value });
     await expect(transaction).to.emit(NFT, "Transfer").withArgs(constants.AddressZero, other.address, 0);
     mintedCount++;

     const balance = (await ProxyWithOtherSigner.balanceOf(other.address)).toNumber();
     expect(balance).to.be.equal(mintedCount);
   });

   it("Must return correct tokenURI for minted token", async () => {
     const tokenId = 0;
     const tokenURI = await ProxyWithOtherSigner.tokenURI(tokenId);

     expect(tokenURI).to.be.equal(batchesInfo[0].url + tokenId);
   });

   it("Must get intervals for minted tokens", async () => {
     const count = batchesInfo[0].count;
     const value = await ProxyWithOtherSigner.price();

     for (let i = 0; i < count; i++) await ProxyWithOtherSigner.mint({ value });
     mintedCount += count;

     const balance = (await ProxyWithOtherSigner.balanceOf(other.address)).toNumber();
     expect(balance).to.be.equal(mintedCount);

     const { baseURIs, endsOfIntervals } = await NFT.getMintedIntervals();

     expect(baseURIs.length).to.be.greaterThan(1);
     expect(endsOfIntervals.length).to.be.equal(baseURIs.length);
     const intervalsCount = baseURIs.length;

     const end = endsOfIntervals[intervalsCount - 1];
     expect(end).to.be.equal(mintedCount);

     let tokenId = 0;
     for (let i = 0; i < intervalsCount; i++) {
       const baseURI = baseURIs[i];
       const endOfInterval = endsOfIntervals[i].toNumber();

       for (; tokenId < endOfInterval; tokenId++) {
         const tokenURI = await ProxyWithOtherSigner.tokenURI(tokenId);
         expect(tokenURI).to.be.equal(baseURI + tokenId);
       }
     }
   });

  it("Must send all ETH to charity address on minted", async () => {
    const prevBalance = await charityMock.getBalance();

    const value = await ProxyWithOtherSigner.price();

    await ProxyWithOtherSigner.mint({ value });
    mintedCount++;

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
});

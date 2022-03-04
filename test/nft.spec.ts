import { expect } from "chai";
import { ethers, upgrades } from "hardhat";
import { Contract } from "ethers";

import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";
import { MuseumOfHistory, MuseumOfHistory__factory } from "../typechain";

describe("Upgradable NFT controlled through UUPS Proxy", function () {
  let owner: SignerWithAddress, other: SignerWithAddress;
  let NFT: MuseumOfHistory;
  let ProxyAddress: string;
  let ProxyWithOtherSigner: Contract;

  before("Deploy NFT proxied using UUPS Proxy", async () => {
    [owner, other] = await ethers.getSigners();
    const Factory = new MuseumOfHistory__factory(owner);

    NFT = await upgrades.deployProxy(Factory, [], {
      kind: "uups",
    }) as MuseumOfHistory;
    ProxyAddress = NFT.address;
    ProxyWithOtherSigner = NFT.connect(other);
  });

  it("Vanilla test", async () => {
    console.log(await NFT.name());
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

//   it("Must support charity address changing", async () => {
//     // todo
//   });

//   it("Must support adding new batch with correct indexing", async () => {
//     // todo
//   });

//   it("Must return correct tokenURI for uploaded batches", async () => {
//     // todo
//   });

});

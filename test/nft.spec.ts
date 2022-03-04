import { expect } from "chai";
import { ethers, upgrades } from "hardhat";
import { Contract } from "ethers";

import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";


describe("Upgradable NFT controlled through UUPS Proxy", function () {
//   let owner: SignerWithAddress, other: SignerWithAddress;
//   let Proxy: Contract;
//   let ProxyAddress: string;
//   let ProxyWithOtherSigner: Contract;

//   before("Deploy NFT proxied using UUPS Proxy", async () => {
//     [owner, other] = await ethers.getSigners();
//     const FactoryV1 = new NFTV1__factory(owner);

//     Proxy = await upgrades.deployProxy(FactoryV1, [owner.address], {
//       kind: "uups",
//       initializer: "init",
//     });
//     ProxyAddress = Proxy.address;
//     ProxyWithOtherSigner = Proxy.connect(other);
//   });

//   it("Must not support features of any contract differing from current implementation", async () => {
//     // test that Proxy doesn't support v2 functionality
//     const ProxyV2 = NFTV2__factory.connect(ProxyAddress, owner);
//     expect(ProxyV2.val()).to.be.revertedWith(
//       "function selector was not recognized and there's no fallback function"
//     );
//   });

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

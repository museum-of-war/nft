import { task } from "hardhat/config";
// import { deploy, upgrade } from "./nft";

task("accounts", "Prints the list of accounts", async (args, hre) => {
  const accounts = await hre.ethers.getSigners();

  for (const account of accounts) {
    const balance = await account.getBalance();
    console.log(`${account.address}: ${balance}`);
  }
});

// task("deploy", "deploy upgradable nft", async (args, hre) => {
//   const [owner] = await hre.ethers.getSigners();
//   await deploy(hre, owner);
// });

// task(
//   "upgrade",
//   "deploy latest version of the upgradable nft",
//   async (args, hre) => {
//     const [owner] = await hre.ethers.getSigners();
//     // if contract is already deployed by this signer, it will return deployed instance
//     const nft = await deploy(hre, owner);
//     await upgrade(hre, owner, nft.address);
//   }
// );

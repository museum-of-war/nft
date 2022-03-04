import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";
import { HardhatRuntimeEnvironment } from "hardhat/types";
import { MuseumOfHistory, MuseumOfHistory__factory } from "../typechain";

export async function compile(hre: HardhatRuntimeEnvironment) {
  await hre.run("compile");
}

export async function deploy(
  hre: HardhatRuntimeEnvironment,
  signer: SignerWithAddress
): Promise<MuseumOfHistory> {
  const Factory = new MuseumOfHistory__factory(signer);
  const Proxy = await hre.upgrades.deployProxy(Factory, [signer.address], {
    kind: "uups",
    initializer: "init",
  });
  console.log(`NFT deployed at ${Proxy.address}`);
  return Proxy as MuseumOfHistory;
}

export async function upgrade(
  hre: HardhatRuntimeEnvironment,
  signer: SignerWithAddress,
  proxyAddress: string
) {
  const Factory = new MuseumOfHistory__factory(signer);
  await hre.upgrades.upgradeProxy(proxyAddress, Factory, {
    kind: "uups",
  });
  console.log(`NFT upgraded.`);
}

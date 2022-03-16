import { HardhatUserConfig } from "hardhat/types";
import "@nomiclabs/hardhat-waffle";
import "hardhat-typechain";
import "hardhat-spdx-license-identifier";
import "@symblox/hardhat-abi-gen";
import "@nomiclabs/hardhat-ethers";
import "@openzeppelin/hardhat-upgrades";
import { config as dotenv } from "dotenv";
dotenv();

const DEFAULT_ACCOUNT_MNEMONIC =
  "siren crystal legend undo cattle comfort lazy cargo move into flower rocket hammer robot affair razor lens viable expand cat vehicle reduce figure river";

const config: HardhatUserConfig = {
  defaultNetwork: "hardhat",
  solidity: {
    compilers: [{ version: "0.8.7", settings: {} }],
  },
  networks: {
    hardhat: {
      chainId: 31337,
      accounts: {
        mnemonic: process.env.ACCOUNT_MNEMONIC || DEFAULT_ACCOUNT_MNEMONIC,
        path: `m/44'/60'/0'/0`,
        initialIndex: 0,
        count: 10,
      },
    },
    // eth: {
    //   chainId: 1,
    //   accounts: {
    //     mnemonic: process.env.ACCOUNT_MNEMONIC || DEFAULT_ACCOUNT_MNEMONIC,
    //     path: `m/44'/60'/0'/0`,
    //     initialIndex: 0,
    //     count: 10,
    //   },
    // },
  },
  spdxLicenseIdentifier: {
    overwrite: true,
    runOnCompile: true,
  },
};
export default config;

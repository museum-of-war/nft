import { expect } from "chai";
import { ethers } from "hardhat";

import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";
import {
    FairXYZMH,
    FairXYZMH__factory,
    FairXYZWallets,
    FairXYZWallets__factory,
} from "../typechain";
import { BigNumber, constants } from "ethers";

describe("Meta History", function () {
    const initialPrice = constants.WeiPerEther.div(10);
    const maxTokens = 100;
    const mintsPerWallet = 5;
    const initialCharityAddress = "0x165CD37b4C644C2921454429E7F9358d18A45e14";
    let owner: SignerWithAddress,
        signer: SignerWithAddress,
        other: SignerWithAddress,
        charity: SignerWithAddress,
        withdraw: SignerWithAddress;
    let Wallets: FairXYZWallets;
    let WalletsWithOtherSigner: FairXYZWallets;
    let MH: FairXYZMH;
    let MHWithOtherSigner: FairXYZMH;

    before("Deploy contracts", async () => {
        [owner, signer, other, charity, withdraw] = await ethers.getSigners();
        const FactoryW = new FairXYZWallets__factory(owner);
        const FactoryMH = new FairXYZMH__factory(owner);

        Wallets = await FactoryW.deploy(owner.address, initialCharityAddress);
        WalletsWithOtherSigner = Wallets.connect(other);

        MH = await FactoryMH.deploy(initialPrice, maxTokens,
            "Museum of History", "MH",
            mintsPerWallet, Wallets.address, initialCharityAddress
        );
        MHWithOtherSigner = MH.connect(other);
    });

    it("Wallets must be initialized", async () => {
        expect(await Wallets.view_signer()).to.be.equal(owner.address);
        expect(await Wallets.view_withdraw()).to.be.equal(initialCharityAddress);
    });

    it("Only owner is allowed to change signer address", async () => {
        await expect(
            WalletsWithOtherSigner.change_signer(signer.address)
        ).to.be.revertedWith("Ownable: caller is not the owner");

        await Wallets.change_signer(signer.address);

        expect(await Wallets.view_signer()).to.be.equal(signer.address);
    });

    it("Only owner is allowed to change withdraw address", async () => {
        await expect(
            WalletsWithOtherSigner.change_withdraw(withdraw.address)
        ).to.be.revertedWith("Ownable: caller is not the owner");

        await Wallets.change_withdraw(withdraw.address);

        expect(await Wallets.view_withdraw()).to.be.equal(withdraw.address);
    });
});

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
    const name = "Museum of History";
    const symbol = "MH";
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

        MH = await FactoryMH.deploy(initialPrice, maxTokens, name, symbol,
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

    it("MH must be initialized", async () => {
        expect(await MH.owner()).to.be.equal(owner.address);
        expect(await MH.ukraineAddress()).to.be.equal(initialCharityAddress);
        expect(await MH.view_Ukraine()).to.be.equal(initialCharityAddress); // looks like a duplicate
        expect(await MH.name()).to.be.equal(name);
        expect(await MH.symbol()).to.be.equal(symbol);
        expect(await MH.price()).to.be.equal(initialPrice);
    });

    it("Only owner is allowed to unpause", async () => {
        await expect(
            MHWithOtherSigner.unpause()
        ).to.be.revertedWith("ERROR");

        const transaction = MH.unpause();

        await expect(transaction).to.emit(MH, "Unpaused").withArgs(owner.address);
    });

    it("MH must mint", async () => {
        const nonce = await MH.view_block_number();
        const blockNumber = await ethers.provider.getBlockNumber();
        expect(nonce.toNumber()).to.be.equal(blockNumber); // it is possible to get block number without adding function

        const numberOfTokens = 1;
        const price = await MH.price();

        const messageHash = ethers.utils.solidityKeccak256(['address', 'uint256', 'uint256'],
            [other.address, numberOfTokens, nonce]
        );
        const signature = await signer.signMessage(ethers.utils.arrayify(messageHash));

        const transaction = MHWithOtherSigner.mint(signature, nonce, numberOfTokens, { value: price });

        await expect(transaction).to.emit(MHWithOtherSigner, "Transfer")
            .withArgs(constants.AddressZero, other.address, 1);
    });
});

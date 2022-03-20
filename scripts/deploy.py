from brownie import accounts, FairXYZWallets, FairXYZMH

def main():

    deployer_account = accounts.load('TestNet')

    # Deploy the contract where multi-sig wallet defines Signer wallets
    FairXYZWallets_ = FairXYZWallets.deploy(deployer_account, deployer_account, {'from': deployer_account}, publish_source = True)
    print("Wallets deployed at: ", FairXYZWallets_.address)

    price_eth = 0.015
    NFTs_on_sale = 10000 
    Name_of_collection = "MetaHistory" 
    Symbol_of_collection = "MHXYZ"
    Mints_per_wallet = "20"
    Interface_address = FairXYZWallets_.address
    Ukraine_wallet_address = "0x165CD37b4C644C2921454429E7F9358d18A45e14"

    # Deploy the MetaHistory contract
    FairXYZMH_ = FairXYZMH.deploy(price_eth * 10**18, NFTs_on_sale, Name_of_collection, Symbol_of_collection,
                                Mints_per_wallet, Interface_address, Ukraine_wallet_address, {'from': deployer_account},
                                publish_source = True)

    print("Contract deployed at: ", FairXYZMH_.address)
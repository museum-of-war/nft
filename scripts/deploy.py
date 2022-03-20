from brownie import accounts, FairXYZWallets, FairXYZMH

def main():

    # If testing on ganache, use accounts[0]
    deployer_account = accounts[0] 

    # If deploying on mainnet, use .load method
    # deployer_account = accounts.load('TestNet)

    if deployer_account == accounts[0]:
        publish_source = False
    
    else:
        publish_source = True

    # Deploy the contract where multi-sig wallet defines Signer wallets
    FairXYZWallets_ = FairXYZWallets.deploy("0xb403d77946B4Ac4FC7CA2EE1059e73f1b72D6e93", "0x165CD37b4C644C2921454429E7F9358d18A45e14",
     {'from': deployer_account}, publish_source = publish_source)
    print("Wallets deployed at: ", FairXYZWallets_.address)

    price_eth = 0.15 # in ethereum
    NFTs_on_sale = 10000 # size of collection
    Name_of_collection = "MetaHistory" # Collection name
    Symbol_of_collection = "MHXYZ" # Collection ticker
    Mints_per_wallet = "20" # Maximum number of mints recommended per wallet (recommended 5-20)
    Interface_address = FairXYZWallets_.address # Address of wallet reference contracts, 
    Ukraine_wallet_address = "0x165CD37b4C644C2921454429E7F9358d18A45e14" # Wallet for Ukrainian government

    # Deploy the MetaHistory contract
    FairXYZMH_ = FairXYZMH.deploy(price_eth * 10**18, NFTs_on_sale, Name_of_collection, Symbol_of_collection,
                                Mints_per_wallet, Interface_address, Ukraine_wallet_address, {'from': deployer_account},
                                publish_source = publish_source)

    print("Contract deployed at: ", FairXYZMH_.address)
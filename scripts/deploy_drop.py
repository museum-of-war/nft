from brownie import accounts, SelectiveDropMHv2

def main():

    # If testing on ganache, use accounts[0]
    # deployer_account = accounts[0]
    # If deploying on mainnet, use .load method
    deployer_account = accounts.load('eth-account') # change to your local account from "brownie accounts list"

    publish_source = True # to publish source code to Etherscan

    price_eth = 0.3 # in ethereum
    NFTs_on_sale = 50 # initial size of collection
    Max_copies = 2 # TODO maxSupply_ how many copies of the NFT can be minted
    Name_of_collection = "Meta History 9" # Collection name
    Symbol_of_collection = "MH9" # Collection ticker
    Mints_per_wallet = 50 # Maximum number of mints recommended per wallet (recommended 5-20)
    withdrawAddress_ = "0xa81E4bC05E57ad79514f56546992D46aDF6aD446" #FairXYZWallets_.address # Address of wallet reference contracts,
    startTime_ = 1675591200 # TODO start time of sale
    uri_ = 'ipfs://Qmf73JZRDCso33UvvJn2GSGJaiNx2Mqkf9CV96rUiYtpK4/{id}'

    # Deploy the MetaHistory contract
    FairXYZMH_ = SelectiveDropMHv2.deploy(price_eth * 10**18,
                                NFTs_on_sale,
                                Max_copies,
                                Name_of_collection,
                                Symbol_of_collection,
                                Mints_per_wallet,
                                uri_,
                                startTime_,
                                withdrawAddress_,
                                {'from': deployer_account},
                                publish_source = publish_source)

    print("Contract deployed at: ", FairXYZMH_.address)

from brownie import accounts, network, SelectiveDropMHv2

def main():
    target_network = network.show_active()

    if target_network == 'goerli':
        deployer = accounts.load('test') # replace with your goerli account
        publish_source = False
    elif target_network == 'mainnet':
        deployer = accounts.load('mainnet')
        publish_source = True # to publish source code to Etherscan
    else:
        raise Exception('use `brownie --network goerli` or `brownie --network mainnet` to run this script')

    print("Deployer:", deployer)
    print("Balance:", deployer.balance() / 10**18, "ETH")

    price_eth = 0.3 # in ETH
    NFTs_on_sale = 50 # initial size of collection
    max_copies = 2 # TODO maxSupply_ how many copies of the NFT can be minted
    collection_name = "Meta History 11" # Collection name
    collection_symbol = "MH11" # Collection ticker
    mints_per_wallet = 50 # Maximum number of mints recommended per wallet (recommended 5-20)
    startTime = 1680362400 # TODO start time of sale
    withdrawAddress = "0xf9b6Ee27527c9D44D21c1ceA0D841440E2507Be4"
    metadata_cid = "QmTgfEcg6vqHMhw2pva3aRJDbeiSqBqCNJfX3cRQPpKhd8" 

    # Deploy the MetaHistory contract
    drop_11 = SelectiveDropMHv2.deploy(
        price_eth * 10**18,
        NFTs_on_sale,
        max_copies,
        collection_name,
        collection_symbol,
        mints_per_wallet,
        "ipfs://" + metadata_cid + "/{id}",
        startTime,
        withdrawAddress,
    { 'from': deployer }, publish_source = publish_source)

    print("Contract deployed at:", drop_11.address)

    if target_network == 'goerli':
        print("Airdrop...")
        drop_11.airdrop(list(range(1, 51)), deployer, { 'from': deployer })

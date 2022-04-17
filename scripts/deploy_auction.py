from brownie import accounts, NFTAuction, FairXYZMH, Prospect100MH


def create_auction(owner, auction, collection, token_id, fee_address):
    collection.approve(auction.address, token_id, {'from': owner})

    auction.createNewNftAuction(
        collection.address,
        token_id,
        "0x0000000000000000000000000000000000000000",
        0.15 * 10**18,
        10 * 10**18,
        86400 * 5,  # 5 days
        100,  # 1.00 %
        [fee_address],
        [10000],  # 100.00 %
        {'from': owner}
    )

def main():

    # If testing on ganache, use accounts[0]
    # deployer_account = accounts[0]

    # If deploying on mainnet, use .load method
    deployer_account = accounts.load('mainnet')

    publish_source = True

    first_drop_address = "0xD3228e099E6596988Ae0b73EAa62591c875e5693"
    georgia_address = "0x5DC23613fD54A87C3b8A7134534110F5180433C8"
    prospect_100_address = "0x932aEAc0eEBaA1fE8fdB53C4f81312cBA5F771A8"

    auction_recipient_address = "0xEDd9Fa9ec9247699dB95De38A06f2DcbEed8423a"

    auction = NFTAuction.deploy([first_drop_address, georgia_address, prospect_100_address],
                                {'from': deployer_account}, publish_source=publish_source)

    print("Auction deployed at: ", auction.address)

    first_drop = FairXYZMH.at(first_drop_address, deployer_account)
    prospect_100 = Prospect100MH.at(prospect_100_address, deployer_account)

    for i in range(1, 5):
        create_auction(deployer_account, auction, first_drop, i, auction_recipient_address)

    for i in range(2, 13):
        create_auction(deployer_account, auction, prospect_100, i, auction_recipient_address)

    print("Auctions created!")

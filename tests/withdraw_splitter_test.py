# noinspection PyUnresolvedReferences
from fixtures import *


def test_receive_and_withdraw_success(WithdrawSplitter, owner, other, stranger, artist):
    amount = '0.175 ether'  # 17.5% = 20% minus 2.5% for OpenSea
    ukraine_part = 100  # 10%
    other_part = 75  # 7.5%

    withdraw_splitter = WithdrawSplitter.deploy(artist.address, ukraine_part, other_part, {'from': owner},
                                                publish_source=False)
    stranger.transfer(withdraw_splitter.address, amount)

    artist_balance_before = artist.balance()
    withdraw_splitter.withdraw({'from': other})

    assert artist.balance() - artist_balance_before == '0.075 ether'


def test_fallback_and_withdraw_success(WithdrawSplitter, owner, other, stranger, artist):
    amount = '0.175 ether'  # 17.5% = 20% minus 2.5% for OpenSea
    ukraine_part = 100  # 10%
    other_part = 75  # 7.5%

    withdraw_splitter = WithdrawSplitter.deploy(artist.address, ukraine_part, other_part, {'from': owner},
                                                publish_source=False)
    stranger.transfer(withdraw_splitter.address, amount, data=str.encode("Some data here"))

    artist_balance_before = artist.balance()
    withdraw_splitter.withdraw({'from': other})

    assert artist.balance() - artist_balance_before == '0.075 ether'

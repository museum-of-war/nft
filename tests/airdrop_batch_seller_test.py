import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_buy_first_drop_success(airdrop_batch_seller, meta_history, other):
    tokens_count = 5
    price = airdrop_batch_seller.tokenPrice()

    airdrop_batch_seller.buyFirstDropTokens(tokens_count, {'from': other, 'value': tokens_count * price})

    assert meta_history.balanceOf(other.address) == tokens_count


def test_buy_second_drop_success(airdrop_batch_seller, drop, other):
    tokens_count = 5
    price = airdrop_batch_seller.tokenPrice()

    airdrop_batch_seller.buySecondDropTokens(tokens_count, {'from': other, 'value': tokens_count * price})

    assert drop.balanceOf(other.address) == tokens_count


def test_buy_first_drop_not_enough_eth(airdrop_batch_seller, other):
    tokens_count = 5
    price = airdrop_batch_seller.tokenPrice()

    with brownie.reverts("Not enough ETH"):
        airdrop_batch_seller.buyFirstDropTokens(tokens_count, {'from': other, 'value': (tokens_count - 1) * price})


def test_buy_second_drop_not_enough_eth(airdrop_batch_seller, other):
    tokens_count = 5
    price = airdrop_batch_seller.tokenPrice()

    with brownie.reverts("Not enough ETH"):
        airdrop_batch_seller.buySecondDropTokens(tokens_count, {'from': other, 'value': (tokens_count - 1) * price})


def test_return_ownerships_success(airdrop_batch_seller, meta_history, drop, owner):
    airdrop_batch_seller.returnOwnerships({'from': owner})

    assert meta_history.owner() == owner.address
    assert drop.owner() == owner.address


def test_return_ownerships_wrong_owner(airdrop_batch_seller, other):
    with brownie.reverts("Ownable: caller is not the owner"):
        airdrop_batch_seller.returnOwnerships({'from': other})

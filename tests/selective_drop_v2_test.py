import pytest
import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_cannot_mint_if_not_started(chain, owner, SelectiveDropMHv2, other):
    future_timestamp = chain.time() + 3600
    selective_drop_v2 = SelectiveDropMHv2.deploy(defaultTokenPrice, fifthDropTokensCount, fifthDropEditionsCount,
                                                 "Meta History 5", "MH5", 100, "uri_base/{id}", future_timestamp,
                                                 "0xc47f5F962b6816d204cb6DbFfbC78d146b42d66c", {'from': owner},
                                                 publish_source=False)
    with brownie.reverts("Minting is not started yet!"):
        selective_drop_v2.mint([1], {'from': other})


def test_withdraw_success(owner, SelectiveDropMHv2, other, stranger, withdraw):
    withdraw_address = withdraw.address
    selective_drop_v2 = SelectiveDropMHv2.deploy(defaultTokenPrice, fifthDropTokensCount, fifthDropEditionsCount,
                                                 "Meta History 5", "MH5", 100, "uri_base/{id}", 0,
                                                 withdraw_address, {'from': owner}, publish_source=False)

    price = selective_drop_v2.price()

    balance_before = withdraw.balance()

    selective_drop_v2.mint([1], {'from': other, 'value': price})
    selective_drop_v2.withdraw({'from': stranger})

    balance_after = withdraw.balance()

    assert balance_after - balance_before == price


@pytest.mark.parametrize('tokens_ids', [[1], [1, 2], [7, 7, 7], [1, 50, 100]])
def test_airdrop_success(selective_drop_v2, owner, other, tokens_ids):
    selective_drop_v2.airdrop(tokens_ids, other.address, {'from': owner})
    assert selective_drop_v2.viewMinted() == len(tokens_ids)
    assert selective_drop_v2.balanceOf(other.address) == len(tokens_ids)
    supplies = {}
    for token_id in tokens_ids:
        supplies[token_id] = supplies.get(token_id, 0) + 1
    for token_id in supplies:
        supply = supplies[token_id]
        assert selective_drop_v2.totalSupply(token_id) == supply
        assert selective_drop_v2.balanceOf(other.address, token_id) == supply


def test_airdrop_invalid_owner(selective_drop_v2, other):
    tokens_ids = [1, 2, 3]

    with brownie.reverts("Ownable: caller is not the owner"):
        selective_drop_v2.airdrop(tokens_ids, other.address, {'from': other})


@pytest.mark.parametrize('tokens_ids', [[1], [1, 2], [7, 7, 7], [1, 50, 100]])
def test_mint(selective_drop_v2, other, tokens_ids):
    tokens_count = len(tokens_ids)
    price = selective_drop_v2.price() * tokens_count
    selective_drop_v2.mint(tokens_ids, {'from': other, 'value': price})
    assert selective_drop_v2.balanceOf(other.address) == tokens_count
    assert selective_drop_v2.viewMinted() == tokens_count
    supplies = {}
    for token_id in tokens_ids:
        supplies[token_id] = supplies.get(token_id, 0) + 1
    for token_id in supplies:
        supply = supplies[token_id]
        assert selective_drop_v2.totalSupply(token_id) == supply
        assert selective_drop_v2.balanceOf(other.address, token_id) == supply


@pytest.mark.parametrize('tokens_ids', [[1], [1, 2], [7, 7, 7], [1, 50, 100]])
def test_mint_to(selective_drop_v2, other, stranger, tokens_ids):
    tokens_count = len(tokens_ids)
    price = selective_drop_v2.price() * tokens_count
    selective_drop_v2.mintTo(tokens_ids, stranger, {'from': other, 'value': price})
    assert selective_drop_v2.balanceOf(stranger.address) == tokens_count
    assert selective_drop_v2.viewMinted() == tokens_count
    supplies = {}
    for token_id in tokens_ids:
        supplies[token_id] = supplies.get(token_id, 0) + 1
    for token_id in supplies:
        supply = supplies[token_id]
        assert selective_drop_v2.totalSupply(token_id) == supply
        assert selective_drop_v2.balanceOf(stranger.address, token_id) == supply


@pytest.mark.parametrize('tokens_ids', [[0], [0, 1, 2], [0, 0, 0], [100, 101, 10000]])
def test_mint_out_of_range(selective_drop_v2, other, tokens_ids):
    tokens_count = len(tokens_ids)
    price = selective_drop_v2.price() * tokens_count

    with brownie.reverts("Token ID is out of range!"):
        selective_drop_v2.mint(tokens_ids, {'from': other, 'value': price})


@pytest.mark.parametrize('token_id', [1, 2, 99, 100])
def test_mint_too_many_same_tokens(selective_drop_v2, other, token_id):
    tokens_count = selective_drop_v2.maxSupply() + 1
    tokens_ids = [token_id] * tokens_count
    price = selective_drop_v2.price() * tokens_count

    with brownie.reverts("This amount exceeds the maximum number of NFTs on sale!"):
        selective_drop_v2.mint(tokens_ids, {'from': other, 'value': price})


def test_balance_after_transfer(selective_drop_v2, other, stranger):
    price = selective_drop_v2.price()
    selective_drop_v2.mint([1], {'from': other, 'value': price})
    selective_drop_v2.mint([2], {'from': stranger, 'value': price})
    selective_drop_v2.safeTransferFrom(other.address, stranger.address, 1, 1, '0x00', {'from': other})
    assert selective_drop_v2.balanceOf(other.address) == 0
    assert selective_drop_v2.balanceOf(stranger.address) == 2


def test_mint_limit(selective_drop_v2, other):
    tokens_count = selective_drop_v2.tokensCount() + 1
    price = selective_drop_v2.price() * tokens_count
    token_ids = list(range(1, tokens_count + 1))

    with brownie.reverts("Token minting limit per transaction exceeded"):
        selective_drop_v2.mint(token_ids, {'from': other, 'value': price})


def test_mint_not_enough_eth(selective_drop_v2, other):
    token_ids = [1]

    with brownie.reverts("You have not sent the required amount of ETH"):
        selective_drop_v2.mint(token_ids, {'from': other, 'value': 0})


def test_change_uri_success(selective_drop_v2, owner):
    new_uri = "new_base_uri/{id}"
    token_id = 1
    selective_drop_v2.changeBaseURI(new_uri, {'from': owner})
    assert selective_drop_v2.uri(token_id) == new_uri


def test_change_uri_invalid_owner(selective_drop_v2, other):
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("Ownable: caller is not the owner"):
        selective_drop_v2.changeBaseURI(new_uri, {'from': other})


def test_change_uri_locked_error(selective_drop_v2, owner):
    selective_drop_v2.lockURI()
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("URI change has been locked"):
        selective_drop_v2.changeBaseURI(new_uri, {'from': owner})

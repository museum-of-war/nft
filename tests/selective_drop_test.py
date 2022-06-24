import pytest
import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_is_paused_after_deploy(selective_drop, other):
    assert selective_drop.paused()
    with brownie.reverts("Pausable: paused"):
        selective_drop.mint([1], {'from': other})


@pytest.mark.parametrize('tokens_ids', [[1], [1, 2], [7, 7, 7], [1, 50, 100]])
def test_airdrop_success(selective_drop, owner, other, tokens_ids):
    selective_drop.unpause()
    selective_drop.airdrop(tokens_ids, other.address, {'from': owner})
    assert selective_drop.viewMinted() == len(tokens_ids)
    assert selective_drop.balanceOf(other.address) == len(tokens_ids)
    supplies = {}
    for token_id in tokens_ids:
        supplies[token_id] = supplies.get(token_id, 0) + 1
    for token_id in supplies:
        supply = supplies[token_id]
        assert selective_drop.totalSupply(token_id) == supply
        assert selective_drop.balanceOf(other.address, token_id) == supply


def test_airdrop_invalid_owner(selective_drop, other):
    tokens_ids = [1, 2, 3]
    selective_drop.unpause()

    with brownie.reverts("Ownable: caller is not the owner"):
        selective_drop.airdrop(tokens_ids, other.address, {'from': other})


@pytest.mark.parametrize('tokens_ids', [[1], [1, 2], [7, 7, 7], [1, 50, 100]])
def test_mint(selective_drop, other, tokens_ids):
    tokens_count = len(tokens_ids)
    price = selective_drop.price() * tokens_count
    selective_drop.unpause()
    selective_drop.mint(tokens_ids, {'from': other, 'value': price})
    assert selective_drop.balanceOf(other.address) == tokens_count
    assert selective_drop.viewMinted() == tokens_count
    supplies = {}
    for token_id in tokens_ids:
        supplies[token_id] = supplies.get(token_id, 0) + 1
    for token_id in supplies:
        supply = supplies[token_id]
        assert selective_drop.totalSupply(token_id) == supply
        assert selective_drop.balanceOf(other.address, token_id) == supply


@pytest.mark.parametrize('tokens_ids', [[0], [0, 1, 2], [0, 0, 0], [100, 101, 10000]])
def test_mint_out_of_range(selective_drop, other, tokens_ids):
    tokens_count = len(tokens_ids)
    price = selective_drop.price() * tokens_count
    selective_drop.unpause()

    with brownie.reverts("Token ID is out of range!"):
        selective_drop.mint(tokens_ids, {'from': other, 'value': price})


@pytest.mark.parametrize('token_id', [1, 2, 99, 100])
def test_mint_too_many_same_tokens(selective_drop, other, token_id):
    tokens_count = selective_drop.maxSupply() + 1
    tokens_ids = [token_id] * tokens_count
    price = selective_drop.price() * tokens_count
    selective_drop.unpause()

    with brownie.reverts("This amount exceeds the maximum number of NFTs on sale!"):
        selective_drop.mint(tokens_ids, {'from': other, 'value': price})


def test_balance_after_transfer(selective_drop, other, stranger):
    price = selective_drop.price()
    selective_drop.unpause()
    selective_drop.mint([1], {'from': other, 'value': price})
    selective_drop.mint([2], {'from': stranger, 'value': price})
    selective_drop.safeTransferFrom(other.address, stranger.address, 1, 1, '0x00', {'from': other})
    assert selective_drop.balanceOf(other.address) == 0
    assert selective_drop.balanceOf(stranger.address) == 2


def test_mint_limit(selective_drop, other):
    tokens_count = selective_drop.tokensCount() + 1
    price = selective_drop.price() * tokens_count
    selective_drop.unpause()
    token_ids = list(range(1, tokens_count + 1))

    with brownie.reverts("Token minting limit per transaction exceeded"):
        selective_drop.mint(token_ids, {'from': other, 'value': price})


def test_mint_not_enough_eth(selective_drop, other):
    token_ids = [1]
    selective_drop.unpause()

    with brownie.reverts("You have not sent the required amount of ETH"):
        selective_drop.mint(token_ids, {'from': other, 'value': 0})


def test_change_uri_success(selective_drop, owner):
    new_uri = "new_base_uri/{id}"
    token_id = 1
    selective_drop.changeBaseURI(new_uri, {'from': owner})
    assert selective_drop.uri(token_id) == new_uri


def test_change_uri_invalid_owner(selective_drop, other):
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("Ownable: caller is not the owner"):
        selective_drop.changeBaseURI(new_uri, {'from': other})


def test_change_uri_locked_error(selective_drop, owner):
    selective_drop.lockURI()
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("URI change has been locked"):
        selective_drop.changeBaseURI(new_uri, {'from': owner})

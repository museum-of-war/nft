import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_is_paused_after_deploy(drop, other):
    assert drop.paused()
    with brownie.reverts("Pausable: paused"):
        drop.mint(1, {'from': other})


def test_mint(drop, other):
    tokens_count = 10
    price = drop.price() * tokens_count
    drop.unpause()
    drop.mint(tokens_count, {'from': other, 'value': price})
    assert drop.balanceOf(other.address) == tokens_count
    assert drop.viewMinted() == tokens_count


def test_mint_sequential(DropMH, owner, other, stranger):
    tokens_count = 2
    drop = DropMH.deploy(defaultTokenPrice, tokens_count, secondDropEditionsCount,
                                      "Meta History 2", "MH2", 100, "uri_base/{id}",
                                      {'from': owner}, publish_source=False)

    price = drop.price()
    drop.unpause()

    drop.mint(1, {'from': other, 'value': price})
    drop.mint(1, {'from': stranger, 'value': price})
    assert drop.balanceOf(other.address, 1) == 1
    assert drop.balanceOf(stranger.address, 2) == 1
    assert drop.viewMinted() == 2


def test_balance_after_transfer(drop, other, stranger):
    price = drop.price()
    drop.unpause()
    drop.mint(1, {'from': other, 'value': price})
    drop.mint(1, {'from': stranger, 'value': price})
    drop.safeTransferFrom(other.address, stranger.address, 1, 1, '0x00', {'from': other})
    assert drop.balanceOf(other.address) == 0
    assert drop.balanceOf(stranger.address) == 2


def test_mint_limit(drop, other):
    tokens_count = drop.tokensCount() + 1
    price = drop.price() * tokens_count
    drop.unpause()

    with brownie.reverts("Token minting limit per transaction exceeded"):
        drop.mint(tokens_count, {'from': other, 'value': price})


def test_mint_not_enough_eth(drop, other):
    tokens_count = 1
    drop.unpause()

    with brownie.reverts("You have not sent the required amount of ETH"):
        drop.mint(tokens_count, {'from': other, 'value': 0})


def test_mint_editions(DropMH, owner, other, stranger):
    tokens_count = 5
    drop = DropMH.deploy(defaultTokenPrice, tokens_count, secondDropEditionsCount,
                                      "Meta History 2", "MH2", 100, "uri_base/{id}",
                                      {'from': owner}, publish_source=False)
    drop.unpause()

    price = drop.price() * tokens_count

    drop.mint(tokens_count, {'from': other, 'value': price})
    drop.mint(tokens_count, {'from': stranger, 'value': price})

    assert drop.balanceOf(other.address) == tokens_count
    assert drop.balanceOf(stranger.address) == tokens_count
    assert drop.viewMinted() == tokens_count * 2

    for i in range(1, tokens_count + 1):
        assert drop.balanceOf(other.address, i) == 1
        assert drop.balanceOf(stranger.address, i) == 1

    drop.mint(1, {'from': other, 'value': drop.price()})
    assert drop.balanceOf(other.address, 1) == 2


def test_change_uri_success(drop, owner):
    new_uri = "new_base_uri/{id}"
    token_id = 1
    drop.changeBaseURI(new_uri, {'from': owner})
    assert drop.uri(token_id) == new_uri


def test_change_uri_invalid_owner(drop, other):
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("Ownable: caller is not the owner"):
        drop.changeBaseURI(new_uri, {'from': other})


def test_change_uri_locked_error(drop, owner):
    drop.lockURI()
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("URI change has been locked"):
        drop.changeBaseURI(new_uri, {'from': owner})


def test_set_burner_success(drop, owner, other):
    drop.setBurner(other.address, {'from': owner})
    assert drop.burner() == other.address


def test_set_burner_invalid_owner(drop, other):
    with brownie.reverts("Ownable: caller is not the owner"):
        drop.setBurner(other.address, {'from': other})


def test_burn_success(drop, owner, other, stranger):
    drop.setBurner(other.address, {'from': owner})
    drop.unpause()

    drop.mint(1, {'from': stranger, 'value': drop.price()})

    drop.burn(stranger.address, 1, 1, {'from': other})
    assert drop.balanceOf(stranger.address, 1) == 0


def test_burn_invalid_account(drop, owner, other, stranger):
    with brownie.reverts("Only burner can burn tokens"):
        drop.burn(other.address, 1, 1, {'from': stranger})

    drop.setBurner(other.address, {'from': owner})

    with brownie.reverts("Only burner can burn tokens"):
        drop.burn(other.address, 1, 1, {'from': stranger})

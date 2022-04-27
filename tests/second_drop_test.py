import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_is_paused_after_deploy(second_drop, other):
    assert second_drop.paused()
    with brownie.reverts("Pausable: paused"):
        second_drop.mint(1, {'from': other})


def test_mint(second_drop, other):
    tokens_count = 10
    price = second_drop.price() * tokens_count
    second_drop.unpause()
    second_drop.mint(tokens_count, {'from': other, 'value': price})
    assert second_drop.balanceOf(other.address) == tokens_count
    assert second_drop.viewMinted() == tokens_count


def test_mint_sequential(SecondDropMH, owner, other, stranger):
    tokens_count = 2
    second_drop = SecondDropMH.deploy(defaultTokenPrice, tokens_count, secondDropEditionsCount,
                                      "Meta History 2", "MH2", 100, "uri_base/{id}",
                                      {'from': owner}, publish_source=False)

    price = second_drop.price()
    second_drop.unpause()

    second_drop.mint(1, {'from': other, 'value': price})
    second_drop.mint(1, {'from': stranger, 'value': price})
    assert second_drop.balanceOf(other.address, 1) == 1
    assert second_drop.balanceOf(stranger.address, 2) == 1
    assert second_drop.viewMinted() == 2


def test_balance_after_transfer(second_drop, other, stranger):
    price = second_drop.price()
    second_drop.unpause()
    second_drop.mint(1, {'from': other, 'value': price})
    second_drop.mint(1, {'from': stranger, 'value': price})
    second_drop.safeTransferFrom(other.address, stranger.address, 1, 1, '0x00', {'from': other})
    assert second_drop.balanceOf(other.address) == 0
    assert second_drop.balanceOf(stranger.address) == 2


def test_mint_limit(second_drop, other):
    tokens_count = second_drop.tokensCount() + 1
    price = second_drop.price() * tokens_count
    second_drop.unpause()

    with brownie.reverts("Token minting limit per transaction exceeded"):
        second_drop.mint(tokens_count, {'from': other, 'value': price})


def test_mint_not_enough_eth(second_drop, other):
    tokens_count = 1
    second_drop.unpause()

    with brownie.reverts("You have not sent the required amount of ETH"):
        second_drop.mint(tokens_count, {'from': other, 'value': 0})


def test_mint_editions(SecondDropMH, owner, other, stranger):
    tokens_count = 5
    second_drop = SecondDropMH.deploy(defaultTokenPrice, tokens_count, secondDropEditionsCount,
                                      "Meta History 2", "MH2", 100, "uri_base/{id}",
                                      {'from': owner}, publish_source=False)
    second_drop.unpause()

    price = second_drop.price() * tokens_count

    second_drop.mint(tokens_count, {'from': other, 'value': price})
    second_drop.mint(tokens_count, {'from': stranger, 'value': price})

    assert second_drop.balanceOf(other.address) == tokens_count
    assert second_drop.balanceOf(stranger.address) == tokens_count
    assert second_drop.viewMinted() == tokens_count * 2

    for i in range(1, tokens_count + 1):
        assert second_drop.balanceOf(other.address, i) == 1
        assert second_drop.balanceOf(stranger.address, i) == 1

    second_drop.mint(1, {'from': other, 'value': second_drop.price()})
    assert second_drop.balanceOf(other.address, 1) == 2


def test_change_uri_success(second_drop, owner):
    new_uri = "new_base_uri/{id}"
    token_id = 1
    second_drop.changeBaseURI(new_uri, {'from': owner})
    assert second_drop.uri(token_id) == new_uri


def test_change_uri_invalid_owner(second_drop, other):
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("Ownable: caller is not the owner"):
        second_drop.changeBaseURI(new_uri, {'from': other})


def test_change_uri_locked_error(second_drop, owner):
    second_drop.lockURI()
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("URI change has been locked"):
        second_drop.changeBaseURI(new_uri, {'from': owner})


def test_set_burner_success(second_drop, owner, other):
    second_drop.setBurner(other.address, {'from': owner})
    assert second_drop.burner() == other.address


def test_set_burner_invalid_owner(second_drop, other):
    with brownie.reverts("Ownable: caller is not the owner"):
        second_drop.setBurner(other.address, {'from': other})


def test_burn_success(second_drop, owner, other, stranger):
    second_drop.setBurner(other.address, {'from': owner})
    second_drop.unpause()

    second_drop.mint(1, {'from': stranger, 'value': second_drop.price()})

    second_drop.burn(stranger.address, 1, 1, {'from': other})
    assert second_drop.balanceOf(stranger.address, 1) == 0


def test_burn_invalid_account(second_drop, owner, other, stranger):
    with brownie.reverts("Only burner can burn tokens"):
        second_drop.burn(other.address, 1, 1, {'from': stranger})

    second_drop.setBurner(other.address, {'from': owner})

    with brownie.reverts("Only burner can burn tokens"):
        second_drop.burn(other.address, 1, 1, {'from': stranger})

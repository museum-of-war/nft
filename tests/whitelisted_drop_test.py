import pytest
import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_one_token_free_mint(owner, WhitelistedSelectiveDropMH, other):
    whitelisted_drop = WhitelistedSelectiveDropMH.deploy(0, fourthDropTokensCount, fourthDropEditionsCount,
                                                         "Meta History 4", "MH4", 1, "uri_base/{id}", 0, [other],
                                                         {'from': owner}, publish_source=False)
    whitelisted_drop.mint([1], {'from': other, 'value': 0})
    assert whitelisted_drop.balanceOf(other.address, 1) == 1
    with brownie.reverts("Exceeds number of mints per wallet"):
        whitelisted_drop.mint([2], {'from': other, 'value': 0})


def test_only_whitelisted_can_mint(whitelisted_drop, other, stranger):
    price = whitelisted_drop.price()

    assert whitelisted_drop.whitelistedAddresses(other.address)
    whitelisted_drop.mint([1], {'from': other, 'value': price})
    assert whitelisted_drop.balanceOf(other.address, 1) == 1

    assert not whitelisted_drop.whitelistedAddresses(stranger.address)
    with brownie.reverts("The recipient is not whitelisted!"):
        whitelisted_drop.mint([1], {'from': stranger, 'value': price})


def test_only_owner_can_add_whitelisted(whitelisted_drop, owner, other, stranger):
    assert not whitelisted_drop.whitelistedAddresses(stranger.address)
    whitelisted_drop.addWhitelistedAddresses([stranger.address], {'from': owner})

    assert whitelisted_drop.whitelistedAddresses(stranger.address)

    with brownie.reverts("Ownable: caller is not the owner"):
        whitelisted_drop.addWhitelistedAddresses([stranger.address], {'from': other})


def test_only_owner_can_remove_whitelisted(whitelisted_drop, owner, other, stranger):
    assert whitelisted_drop.whitelistedAddresses(other.address)
    whitelisted_drop.removeWhitelistedAddresses([other.address], {'from': owner})

    assert not whitelisted_drop.whitelistedAddresses(other.address)

    with brownie.reverts("Ownable: caller is not the owner"):
        whitelisted_drop.addWhitelistedAddresses([stranger.address], {'from': other})


def test_whitelist_change_error_on_locked(whitelisted_drop, owner, other, stranger):
    with brownie.reverts("Ownable: caller is not the owner"):
        whitelisted_drop.lockWhitelist({'from': other})

    whitelisted_drop.lockWhitelist({'from': owner})

    with brownie.reverts("Whitelist change has been locked"):
        whitelisted_drop.addWhitelistedAddresses([stranger.address], {'from': owner})

    with brownie.reverts("Whitelist change has been locked"):
        whitelisted_drop.removeWhitelistedAddresses([other.address], {'from': owner})

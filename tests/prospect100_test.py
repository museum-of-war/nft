import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_prospect100_instant_airdrop_success(owner, Prospect100MH):
    instant_airdrop = 4
    prospect100 = Prospect100MH.deploy(instant_airdrop, "Prospect 100", "P100MH",
                                       "uri_base", instant_airdrop,
                                       {'from': owner}, publish_source=False)
    assert prospect100.balanceOf(owner) == instant_airdrop


def test_prospect100_instant_airdrop_too_many(owner, Prospect100MH):
    instant_airdrop = 4
    with brownie.reverts("Too many tokens to airdrop"):
        Prospect100MH.deploy(instant_airdrop - 1, "Prospect 100", "P100MH",
                             "uri_base", instant_airdrop,
                             {'from': owner}, publish_source=False)


def test_prospect100_mint_success(prospect100, other, stranger):
    prospect100.changeMinterAddress(other.address)
    tx = prospect100.tryMint(stranger.address, {'from': other})
    assert tx.return_value[0]
    assert prospect100.balanceOf(stranger) == 1


def test_prospect100_mint_wrong_minter_error(prospect100, other, stranger):
    prospect100.changeMinterAddress(stranger.address)
    with brownie.reverts("Not a minter"):
        prospect100.tryMint(stranger.address, {'from': other})


def test_prospect100_try_mint_too_many(Prospect100MH, owner, other, stranger):
    prospect100 = Prospect100MH.deploy(0, "Prospect 100", "P100MH",
                                       "uri_base", 0,
                                       {'from': owner}, publish_source=False)
    prospect100.changeMinterAddress(other.address)
    tx = prospect100.tryMint(stranger.address, {'from': other})
    assert not tx.return_value[0]
    assert prospect100.balanceOf(stranger) == 0


def test_prospect100_try_mint_last(Prospect100MH, owner, other, stranger):
    instant_airdrop = 4
    prospect100 = Prospect100MH.deploy(instant_airdrop + 1, "Prospect 100", "P100MH",
                                       "uri_base", instant_airdrop,
                                       {'from': owner}, publish_source=False)
    prospect100.changeMinterAddress(other.address)
    tx = prospect100.tryMint(stranger.address, {'from': other})
    assert tx.return_value[0]
    assert prospect100.balanceOf(stranger) == 1

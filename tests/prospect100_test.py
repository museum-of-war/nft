import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_prospect100_instant_airdrop(owner, Prospect100MH):
    instant_airdrop = 4
    prospect100 = Prospect100MH.deploy("Prospect 100", "P100MH",
                                       "uri_base", instant_airdrop,
                                       {'from': owner}, publish_source=False)
    assert prospect100.balanceOf(owner) == instant_airdrop


def test_prospect100_mint_success(prospect100, other, stranger):
    prospect100.changeMinterAddress(other.address)
    prospect100.mint(stranger.address, {'from': other})
    assert prospect100.balanceOf(stranger) == 1


def test_prospect100_mint_wrong_minter_error(prospect100, other, stranger):
    prospect100.changeMinterAddress(stranger.address)
    with brownie.reverts("Not a minter"):
        prospect100.mint(stranger.address, {'from': other})

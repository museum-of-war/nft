import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_airdrop_success(GeorgiaMH, owner, other):
    base_uri = "uri_base/"
    token_id = 1
    instant_airdrop = 5
    georgia = GeorgiaMH.deploy("Meta History: Georgia", "MHG",
                               instant_airdrop, base_uri, other.address, {'from': owner}, publish_source=False)
    assert georgia.balanceOf(other.address) == instant_airdrop
    assert georgia.tokenURI(1) == base_uri + str(token_id)


def test_change_uri_success(georgia, owner):
    new_uri = "new_base_uri/"
    token_id = 1
    georgia.changeBaseURI(new_uri, {'from': owner})
    assert georgia.tokenURI(1) == new_uri + str(token_id)


def test_change_uri_invalid_owner(georgia, other):
    new_uri = "new_base_uri/"
    with brownie.reverts("Ownable: caller is not the owner"):
        georgia.changeBaseURI(new_uri, {'from': other})


def test_change_uri_locked_error(georgia, owner):
    georgia.lockURI()
    new_uri = "new_base_uri/"
    with brownie.reverts("URI change has been locked"):
        georgia.changeBaseURI(new_uri, {'from': owner})

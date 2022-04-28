import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_airdrop_success(CollectionMH, owner, other):
    base_uri = "uri_base/"
    token_id = 1
    instant_airdrop = 5
    collection = CollectionMH.deploy("Meta History: Special", "Special",
                                     instant_airdrop, base_uri, other.address, {'from': owner}, publish_source=False)
    assert collection.balanceOf(other.address) == instant_airdrop
    assert collection.tokenURI(token_id) == base_uri + str(token_id)


def test_change_uri_success(collection, owner):
    new_uri = "new_base_uri/"
    token_id = 1
    collection.changeBaseURI(new_uri, {'from': owner})
    assert collection.tokenURI(token_id) == new_uri + str(token_id)


def test_change_uri_invalid_owner(collection, other):
    new_uri = "new_base_uri/"
    with brownie.reverts("Ownable: caller is not the owner"):
        collection.changeBaseURI(new_uri, {'from': other})


def test_change_uri_locked_error(collection, owner):
    collection.lockURI()
    new_uri = "new_base_uri/"
    with brownie.reverts("URI change has been locked"):
        collection.changeBaseURI(new_uri, {'from': owner})

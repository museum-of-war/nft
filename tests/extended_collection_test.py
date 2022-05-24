import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_airdrop_success(ExtendedCollectionMH, owner, other):
    contract_uri = "contract_uri"
    base_uri = "uri_base/"
    token_id = 1
    instant_airdrop = 5
    extended_collection = ExtendedCollectionMH.deploy("Meta History: Special", "Special",
                                                      contract_uri, base_uri, instant_airdrop, other.address,
                                                      {'from': owner}, publish_source=False)
    assert extended_collection.balanceOf(other.address) == instant_airdrop
    assert extended_collection.contractURI() == contract_uri
    assert extended_collection.tokenURI(token_id) == base_uri + str(token_id)


def test_change_uri_success(extended_collection, owner):
    new_uri = "new_base_uri/"
    token_id = 1
    extended_collection.changeBaseURI(new_uri, {'from': owner})
    assert extended_collection.tokenURI(token_id) == new_uri + str(token_id)


def test_change_contract_uri_success(extended_collection, owner):
    new_uri = "new_contract_uri"
    extended_collection.changeContractURI(new_uri, {'from': owner})
    assert extended_collection.contractURI() == new_uri


def test_change_uri_invalid_owner(extended_collection, other):
    new_uri = "new_base_uri/"
    new_contract_uri = "new_contract_uri"
    with brownie.reverts("Ownable: caller is not the owner"):
        extended_collection.changeBaseURI(new_uri, {'from': other})
    with brownie.reverts("Ownable: caller is not the owner"):
        extended_collection.changeContractURI(new_contract_uri, {'from': other})


def test_change_uri_locked_error(extended_collection, owner):
    extended_collection.lockURI()
    new_uri = "new_base_uri/"
    new_contract_uri = "new_contract_uri"
    with brownie.reverts("URI change has been locked"):
        extended_collection.changeBaseURI(new_uri, {'from': owner})
    with brownie.reverts("URI change has been locked"):
        extended_collection.changeContractURI(new_contract_uri, {'from': owner})

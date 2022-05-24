import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_airdrop_success(SingleTokenMH, owner, other):
    contract_uri = "contract_uri"
    token_uri = "token_uri"
    token_id = 1
    single_token = SingleTokenMH.deploy("Meta History: Single", "Single",
                                        contract_uri, token_uri, other.address,
                                        {'from': owner}, publish_source=False)
    assert single_token.balanceOf(other.address) == 1
    assert single_token.ownerOf(1) == other.address
    assert single_token.ownerOf() == other.address
    assert single_token.contractURI() == contract_uri
    assert single_token.tokenURI(token_id) == token_uri
    assert single_token.tokenURI() == token_uri


def test_change_uri_success(single_token, owner):
    new_uri = "new_token_uri"
    token_id = 1
    single_token.changeBaseURI(new_uri, {'from': owner})
    assert single_token.tokenURI(token_id) == new_uri
    assert single_token.tokenURI() == new_uri


def test_change_contract_uri_success(single_token, owner):
    new_uri = "new_contract_uri"
    single_token.changeContractURI(new_uri, {'from': owner})
    assert single_token.contractURI() == new_uri


def test_change_uri_invalid_owner(single_token, other):
    new_uri = "new_token_uri"
    new_contract_uri = "new_contract_uri"
    with brownie.reverts("Ownable: caller is not the owner"):
        single_token.changeBaseURI(new_uri, {'from': other})
    with brownie.reverts("Ownable: caller is not the owner"):
        single_token.changeContractURI(new_contract_uri, {'from': other})


def test_change_uri_locked_error(single_token, owner):
    old_uri = single_token.tokenURI()
    tx = single_token.lockURI()
    event = tx.events['PermanentURI'][0]
    assert event['_value'] == old_uri
    assert event['_id'] == 1
    new_uri = "new_token_uri"
    new_contract_uri = "new_contract_uri"
    with brownie.reverts("URI change has been locked"):
        single_token.changeBaseURI(new_uri, {'from': owner})
    with brownie.reverts("URI change has been locked"):
        single_token.changeContractURI(new_contract_uri, {'from': owner})

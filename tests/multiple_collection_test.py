import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_airdrop_success(MultipleCollectionMH, owner, other):
    base_uri = "uri_base/{id}"
    tokens_amounts = [1, 2, 3]
    tokens_types = len(tokens_amounts)
    collection = MultipleCollectionMH.deploy("Meta History: Multiple", "MHM", base_uri, other.address, tokens_amounts,
                                             {'from': owner}, publish_source=False)
    assert collection.balanceOf(other.address) == sum(tokens_amounts)
    assert collection.totalSupply() == sum(tokens_amounts)
    assert collection.tokensTypes() == tokens_types
    for i in range(tokens_types):
        assert collection.totalSupply(i + 1) == tokens_amounts[i]
        assert collection.balanceOf(other.address, i + 1) == tokens_amounts[i]
    assert collection.balanceOfBatch([other.address] * tokens_types, list(range(1, tokens_types + 1))) == tokens_amounts
    assert collection.uri(1) == base_uri


def test_change_uri_success(multiple_collection, owner):
    new_uri = "new_base_uri/{id}"
    token_id = 1
    multiple_collection.changeBaseURI(new_uri, {'from': owner})
    assert multiple_collection.uri(token_id) == new_uri


def test_change_uri_invalid_owner(multiple_collection, other):
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("Ownable: caller is not the owner"):
        multiple_collection.changeBaseURI(new_uri, {'from': other})


def test_change_uri_locked_error(multiple_collection, owner):
    multiple_collection.lockURI()
    new_uri = "new_base_uri/{id}"
    with brownie.reverts("URI change has been locked"):
        multiple_collection.changeBaseURI(new_uri, {'from': owner})

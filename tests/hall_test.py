import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_create_and_mint_success(hall, other):
    token_id = 12345
    token_uri = "tokenURI_12345"
    hall.safeCreateAndMint(other.address, token_id, token_uri, "")

    assert hall.ownerOf(token_id) == other.address
    assert hall.balanceOf(other.address) == 1
    assert hall.tokenURI(token_id) == token_uri


def test_create_and_mint_invalid_owner(hall, other):
    token_id = 12345
    with brownie.reverts("Ownable: caller is not the owner"):
        hall.safeCreateAndMint(other.address, token_id, "tokenURI", "", {'from': other})


def test_create_and_mint_same_error(hall, other):
    token_id = 12345
    hall.safeCreateAndMint(other.address, token_id, "tokenURI", "")
    with brownie.reverts("Existent token"):
        hall.safeCreateAndMint(other.address, token_id, "tokenURI", "")


def test_create_success(hall):
    token_id = 12345
    token_uri = "tokenURI_12345"
    hall.create(token_id, token_uri)
    assert hall.tokenURI(token_id) == token_uri
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        hall.ownerOf(token_id)


def test_create_same_error(hall):
    token_id = 12345
    token_uri = "tokenURI_12345"
    hall.create(token_id, token_uri)
    with brownie.reverts("Existent token"):
        hall.create(token_id, token_uri)


def test_change_uri_success(hall):
    token_id = 12345
    token_uri1 = "tokenURI_old"
    token_uri2 = "tokenURI_new"
    hall.create(token_id, token_uri1)
    hall.changeURI(token_id, token_uri2)
    assert hall.tokenURI(token_id) == token_uri2


def test_change_uri_nonexistent_error(hall):
    token_id = 12345
    token_uri = "tokenURI"
    with brownie.reverts("Nonexistent token"):
        hall.changeURI(token_id, token_uri)


def test_lock_uri_success(hall):
    token_id = 12345
    token_uri1 = "tokenURI_12345"
    token_uri2 = "tokenURI_wrong"
    hall.create(token_id, token_uri1)
    hall.lockURI(token_id)
    with brownie.reverts("URI change has been locked"):
        hall.changeURI(token_id, token_uri2)
    assert hall.tokenURI(token_id) == token_uri1


def test_lock_uri_nonexistent_error(hall):
    token_id = 12345
    with brownie.reverts("Nonexistent token"):
        hall.lockURI(token_id)


def test_mint_success(hall, other):
    token_id = 12345
    token_uri = "tokenURI_12345"
    hall.create(token_id, token_uri)
    hall.safeMint(other.address, token_id, "")

    assert hall.ownerOf(token_id) == other.address
    assert hall.balanceOf(other.address) == 1
    assert hall.tokenURI(token_id) == token_uri


def test_mint_nonexistent_error(hall, other):
    token_id = 12345
    with brownie.reverts("Nonexistent token"):
        hall.safeMint(other.address, token_id, "")

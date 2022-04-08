import pytest
import brownie


specialTokensCount = 4
elementsCount = 9
editionsCount = 11
totalTokensCount = specialTokensCount + elementsCount * editionsCount
prospect100AirdropCount = 12

@pytest.fixture
def owner(accounts):
    return accounts[0]


@pytest.fixture
def signer_mock(accounts):
    return accounts[1]


@pytest.fixture
def charity_mock(accounts):
    return accounts[2]


@pytest.fixture
def withdraw(accounts):
    return accounts[3]


@pytest.fixture
def other(accounts):
    return accounts[4]


@pytest.fixture
def stranger(accounts):
    return accounts[5]


@pytest.fixture
def wallets(owner, signer_mock, withdraw, FairXYZWallets):
    return FairXYZWallets.deploy(signer_mock, withdraw, {'from': owner}, publish_source=False)


@pytest.fixture
def meta_history(owner, charity_mock, FairXYZMH, wallets):
    return FairXYZMH.deploy(0.15 * 10 ** 18, totalTokensCount, "MetaHistory", "MHXYZ",
                            0, wallets.address, 0, "uri_base",
                            {'from': owner}, publish_source=False)


@pytest.fixture
def prospect100(owner, Prospect100MH):
    return Prospect100MH.deploy("Prospect 100", "P100MH",
                                "uri_base", prospect100AirdropCount,
                                {'from': owner}, publish_source=False)


@pytest.fixture
def merger(owner, MergerMH, meta_history, prospect100):
    merger_contract = MergerMH.deploy("MetaHistory: High Levels", "MHHL",
                           meta_history.address, prospect100.address, "uri_base",
                           specialTokensCount, elementsCount, editionsCount,
                           {'from': owner}, publish_source=False)
    prospect100.changeMinterAddress(merger_contract.address)
    return merger_contract


def test_is_paused_after_deploy(meta_history, other):
    assert meta_history.paused()
    with brownie.reverts("Pausable: paused"):
        meta_history.mint("0", 12345, 1, {'from': other})


def test_instant_airdrop(owner, FairXYZMH, wallets):
    instant_airdrop = 4
    meta_history = FairXYZMH.deploy(0.15 * 10 ** 18, 100, "MetaHistory", "MHXYZ", 0,
                                    wallets.address, instant_airdrop, "uri_base",
                                    {'from': owner}, publish_source=False)
    assert meta_history.balanceOf(owner) == 4


def test_airdrop(meta_history, other):
    meta_history.airdrop([other], 1)
    assert meta_history.balanceOf(other) == 1


def test_mint(meta_history, other, signer_mock):
    nonce = brownie.web3.eth.block_number
    assert nonce == meta_history.view_block_number()
    price = meta_history.price()
    tokens_count = 1
    hash = brownie.web3.solidityKeccak(
        ["address", "uint256", "uint256", "address"],
        [other.address, tokens_count, nonce, meta_history.address]
    )
    signature = brownie.web3.eth.sign(signer_mock.address, hash)
    meta_history.unpause()
    meta_history.mint(signature, nonce, tokens_count, {'from': other, 'value': price})
    assert meta_history.balanceOf(other) == tokens_count


@pytest.mark.parametrize('token_id', [5, 4 + elementsCount, totalTokensCount - elementsCount])
def test_merge_base_success(merger, meta_history, other, token_id):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id, {'from': other})
    meta_history.approve(merger.address, token_id + elementsCount, {'from': other})
    merger.mergeBase(token_id, token_id + elementsCount, {'from': other})
    assert merger.balanceOf(other) == 1


def test_merge_base_wrong_owner_error(merger, meta_history, other, stranger):
    token_id = specialTokensCount + 1
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id, {'from': other})
    meta_history.approve(merger.address, token_id + elementsCount, {'from': other})
    with brownie.reverts("Sender must be an owner"):
        merger.mergeBase(token_id, token_id + elementsCount, {'from': stranger})


@pytest.mark.parametrize('token_id1', [5, 9, 7 + elementsCount])
@pytest.mark.parametrize('token_id2', [8, 6, totalTokensCount])
def test_merge_base_different_error(merger, meta_history, other, token_id1, token_id2):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id1, {'from': other})
    meta_history.approve(merger.address, token_id2, {'from': other})
    with brownie.reverts("Cannot merge different elements"):
        merger.mergeBase(token_id1, token_id2, {'from': other})


@pytest.mark.parametrize('token_id', [5, 50, totalTokensCount])
def test_merge_base_same_error(merger, meta_history, other, token_id):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id, {'from': other})
    meta_history.approve(merger.address, token_id, {'from': other})
    with brownie.reverts("Cannot merge token with self"):
        merger.mergeBase(token_id, token_id, {'from': other})


@pytest.mark.parametrize('token_id1', [1, 2, specialTokensCount])
@pytest.mark.parametrize('token_id2', [1, 5, elementsCount, totalTokensCount])
def test_merge_base_unique_error(merger, meta_history, other, token_id1, token_id2):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id1, {'from': other})
    meta_history.approve(merger.address, token_id2, {'from': other})
    with brownie.reverts("Cannot merge unique token"):
        merger.mergeBase(token_id1, token_id2, {'from': other})


@pytest.mark.parametrize('token_id', [5, 4 + elementsCount, totalTokensCount - 4 * elementsCount])
def test_merge_advanced_success(merger, prospect100, meta_history, other, token_id):
    meta_history.airdrop([other], totalTokensCount)

    token_ids = []

    for i in range(0, 4, 2):
        token_id1 = token_id + i * elementsCount
        token_id2 = token_id + (i + 1) * elementsCount
        meta_history.approve(merger.address, token_id1, {'from': other})
        meta_history.approve(merger.address, token_id2, {'from': other})
        tx = merger.mergeBase(token_id1, token_id2, {'from': other})
        token_ids.append(tx.events["Transfer"][-1]["tokenId"])

    assert merger.balanceOf(other) == 2
    merger.mergeAdvanced(token_ids[0], token_ids[1], {'from': other})
    assert merger.balanceOf(other) == 1
    assert prospect100.balanceOf(other) == 1


def test_merge_advanced_not_owner_error(merger, meta_history, other, stranger):
    meta_history.airdrop([other], totalTokensCount)

    token_ids = []

    for token_id in [specialTokensCount + 1, specialTokensCount + 2 * elementsCount + 1]:
        meta_history.approve(merger.address, token_id, {'from': other})
        meta_history.approve(merger.address, token_id + elementsCount, {'from': other})
        tx = merger.mergeBase(token_id, token_id + elementsCount, {'from': other})
        token_ids.append(tx.events["Transfer"][-1]["tokenId"])

    with brownie.reverts("Sender must be an owner"):
        merger.mergeAdvanced(token_ids[0], token_ids[1], {'from': stranger})


@pytest.mark.parametrize('token_id1', [5, 9, 7 + elementsCount])
@pytest.mark.parametrize('token_id2', [8, 6, totalTokensCount - elementsCount])
def test_merge_advanced_different_error(merger, meta_history, other, token_id1, token_id2):
    meta_history.airdrop([other], totalTokensCount)

    token_ids = []

    for token_id in [token_id1, token_id2]:
        meta_history.approve(merger.address, token_id, {'from': other})
        meta_history.approve(merger.address, token_id + elementsCount, {'from': other})
        tx = merger.mergeBase(token_id, token_id + elementsCount, {'from': other})
        token_ids.append(tx.events["Transfer"][-1]["tokenId"])

    with brownie.reverts("Cannot merge different tokens"):
        merger.mergeAdvanced(token_ids[0], token_ids[1], {'from': other})


@pytest.mark.parametrize('token_id', [5, 4 + elementsCount, totalTokensCount - 4 * elementsCount])
def test_merge_advanced_same_error(merger, meta_history, other, token_id):
    meta_history.airdrop([other], totalTokensCount)

    token_id1 = token_id
    token_id2 = token_id + elementsCount
    meta_history.approve(merger.address, token_id1, {'from': other})
    meta_history.approve(merger.address, token_id2, {'from': other})
    tx = merger.mergeBase(token_id1, token_id2, {'from': other})
    token_id_to_merge = tx.events["Transfer"][-1]["tokenId"]

    with brownie.reverts("Cannot merge token with self"):
        merger.mergeAdvanced(token_id_to_merge, token_id_to_merge, {'from': other})


@pytest.mark.parametrize('token_id', [5, 4 + elementsCount, totalTokensCount - 6 * elementsCount])
def test_merge_advanced_different_levels_error(merger, meta_history, other, token_id):
    meta_history.airdrop([other], totalTokensCount)

    token_ids = []

    for i in range(0, 6, 2):
        token_id1 = token_id + i * elementsCount
        token_id2 = token_id + (i + 1) * elementsCount
        meta_history.approve(merger.address, token_id1, {'from': other})
        meta_history.approve(merger.address, token_id2, {'from': other})
        tx = merger.mergeBase(token_id1, token_id2, {'from': other})
        token_ids.append(tx.events["Transfer"][-1]["tokenId"])

    tx = merger.mergeAdvanced(token_ids[0], token_ids[1], {'from': other})
    high_token_id = tx.events["Transfer"][-2]["tokenId"]

    with brownie.reverts("Cannot merge different levels"):
        merger.mergeAdvanced(high_token_id, token_ids[-1], {'from': other})

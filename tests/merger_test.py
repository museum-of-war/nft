import pytest
import brownie
from fixtures import *


@pytest.mark.parametrize('token_id', [5, 4 + elementsCount, totalTokensCount - 7 * elementsCount])
@pytest.mark.parametrize('count', [2, 3, 8])
def test_merge_base_batch_success(merger, meta_history, prospect100, other, token_id, count):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.setApprovalForAll(merger.address, True, {'from': other})
    merger.mergeBaseBatch([token_id + i * elementsCount for i in range(count)], {'from': other})
    assert merger.balanceOf(other) == 1
    assert prospect100.balanceOf(other) == (1 << (count.bit_length() - 2)) - 1  # 16 will give 7
    assert meta_history.balanceOf(other) == totalTokensCount - (1 << (count.bit_length() - 1))  # burn power of 2


@pytest.mark.parametrize('token_id', [specialTokensCount + 1, specialTokensCount + elementsCount])
@pytest.mark.parametrize('level', [1, 2, editionsCount.bit_length() - 1])
def test_merge_get_token_info(merger, meta_history, other, token_id, level):
    count = 1 << level
    meta_history.airdrop([other], totalTokensCount)
    meta_history.setApprovalForAll(merger.address, True, {'from': other})
    tx = merger.mergeBaseBatch([token_id + i * elementsCount for i in range(count)], {'from': other})
    new_token_id = tx.events["Transfer"][count]["tokenId"]
    assert merger.getTokenInfo(new_token_id) == (token_id, level)


def test_merge_base_batch_wrong_owner_error(merger, meta_history, other, stranger):
    token_id = specialTokensCount + 1
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id, {'from': other})
    meta_history.approve(merger.address, token_id + elementsCount, {'from': other})
    with brownie.reverts("Sender must be an owner"):
        merger.mergeBaseBatch([token_id, token_id + elementsCount], {'from': stranger})


@pytest.mark.parametrize('token_id1', [5, 9, 7 + elementsCount])
@pytest.mark.parametrize('token_id2', [8, 6, totalTokensCount])
def test_merge_base_batch_different_error(merger, meta_history, other, token_id1, token_id2):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id1, {'from': other})
    meta_history.approve(merger.address, token_id2, {'from': other})
    with brownie.reverts("Cannot merge different elements"):
        merger.mergeBaseBatch([token_id1, token_id2], {'from': other})


@pytest.mark.parametrize('token_id', [5, 50, totalTokensCount])
def test_merge_base_batch_not_enough_error(merger, meta_history, other, token_id):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id, {'from': other})
    with brownie.reverts("Not enough tokens"):
        merger.mergeBaseBatch([token_id], {'from': other})


@pytest.mark.parametrize('token_id', [5, 50, totalTokensCount])
@pytest.mark.parametrize('count', [2, 3, 8])
def test_merge_base_batch_same_error(merger, meta_history, other, token_id, count):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id, {'from': other})
    with brownie.reverts("Cannot merge token with self"):
        merger.mergeBaseBatch([token_id for _ in range(count)], {'from': other})


@pytest.mark.parametrize('token_id1', [1, 2, specialTokensCount])
@pytest.mark.parametrize('token_id2', [1, 5, elementsCount, totalTokensCount])
def test_merge_base_batch_unique_error(merger, meta_history, other, token_id1, token_id2):
    meta_history.airdrop([other], totalTokensCount)
    meta_history.approve(merger.address, token_id1, {'from': other})
    meta_history.approve(merger.address, token_id2, {'from': other})
    with brownie.reverts("Cannot merge unique token"):
        merger.mergeBaseBatch([token_id1, token_id2], {'from': other})


@pytest.mark.parametrize('token_id', [5, 4 + elementsCount, totalTokensCount - 4 * elementsCount])
def test_merge_advanced_success(merger, prospect100, meta_history, other, token_id):
    meta_history.airdrop([other], totalTokensCount)

    token_ids = []

    for i in range(0, 4, 2):
        token_id1 = token_id + i * elementsCount
        token_id2 = token_id + (i + 1) * elementsCount
        meta_history.approve(merger.address, token_id1, {'from': other})
        meta_history.approve(merger.address, token_id2, {'from': other})
        tx = merger.mergeBaseBatch([token_id1, token_id2], {'from': other})
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
        tx = merger.mergeBaseBatch([token_id, token_id + elementsCount], {'from': other})
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
        tx = merger.mergeBaseBatch([token_id, token_id + elementsCount], {'from': other})
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
    tx = merger.mergeBaseBatch([token_id1, token_id2], {'from': other})
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
        tx = merger.mergeBaseBatch([token_id1, token_id2], {'from': other})
        token_ids.append(tx.events["Transfer"][-1]["tokenId"])

    tx = merger.mergeAdvanced(token_ids[0], token_ids[1], {'from': other})
    high_token_id = tx.events["Transfer"][-2]["tokenId"]

    with brownie.reverts("Cannot merge different levels"):
        merger.mergeAdvanced(high_token_id, token_ids[-1], {'from': other})

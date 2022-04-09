import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


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

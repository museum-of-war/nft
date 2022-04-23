import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_transfer_and_withdraw_success(chain, StubWithdrawer, owner, other, stranger):
    message = "Wrong network, please, use Ethereum Mainnet"

    nonce = owner.nonce
    withdrawer = StubWithdrawer.deploy(message, {'from': owner, 'nonce': nonce}, publish_source=False)
    withdrawer_address = withdrawer.address

    chain.undo()

    other_balance_before = other.balance()
    stranger_balance_before = other.balance()

    amount = 5 * 10 ** 18

    other.transfer(withdrawer_address, amount)
    stranger.transfer(withdrawer_address, amount)

    withdrawer = StubWithdrawer.deploy(message, {'from': owner, 'nonce': nonce}, publish_source=False)

    with brownie.reverts("Ownable: caller is not the owner"):
        withdrawer.withdraw([other.address], amount * 2, {'from': stranger})

    withdrawer.withdraw([other.address, stranger.address], amount)

    assert other_balance_before == other.balance()
    assert stranger_balance_before == stranger.balance()


def test_receive_revert(withdrawer, other):
    amount = 5 * 10 ** 18
    with brownie.reverts("Wrong network, please, use Ethereum Mainnet"):
        other.transfer(withdrawer.address, amount)


def test_fallback_revert(withdrawer, other):
    amount = 5 * 10 ** 18
    with brownie.reverts("Wrong network, please, use Ethereum Mainnet"):
        other.transfer(withdrawer.address, amount, data=str.encode("Some data here"))

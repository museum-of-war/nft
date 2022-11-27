import brownie
# noinspection PyUnresolvedReferences
from fixtures import *


def test_receive_and_withdraw_success(WithdrawSplitterV2, owner, other, stranger, artist, charity_mock, signer_mock):
    amount = brownie.Wei('1 ether')
    receivers = [charity_mock, artist, signer_mock]
    proportions = [80, 10, 10]
    proportions_sum = sum(proportions)

    withdraw_splitter = WithdrawSplitterV2.deploy(receivers, proportions, {'from': owner}, publish_source=False)
    stranger.transfer(withdraw_splitter.address, amount)

    balances_before = []
    for receiver in receivers:
        balances_before.append(receiver.balance())

    withdraw_splitter.withdraw({'from': other})

    for i in range(len(receivers)):
        assert receivers[i].balance() - balances_before[i] == amount * proportions[i] / proportions_sum


def test_fallback_and_withdraw_success(WithdrawSplitterV2, owner, other, stranger, artist, charity_mock, signer_mock):
    amount = brownie.Wei('1 ether')
    receivers = [charity_mock, artist, signer_mock]
    proportions = [80, 10, 10]
    proportions_sum = sum(proportions)

    withdraw_splitter = WithdrawSplitterV2.deploy(receivers, proportions, {'from': owner}, publish_source=False)
    stranger.transfer(withdraw_splitter.address, amount, data=str.encode("Some data here"))

    balances_before = []
    for receiver in receivers:
        balances_before.append(receiver.balance())

    withdraw_splitter.withdraw({'from': other})

    for i in range(len(receivers)):
        assert receivers[i].balance() - balances_before[i] == amount * proportions[i] / proportions_sum

import pytest
from brownie import network, accounts, exceptions
from scripts.deploy import deploy_fundme
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account


def test_initial_state():
    fund_me = deploy_fundme()
    account = get_account()

    assert fund_me.getBalance() == 0
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_can_fund():
    fund_me = deploy_fundme()
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()

    transaction = fund_me.fund({"from": account, "value": entrance_fee})
    transaction.wait(1)

    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    assert fund_me.getBalance() == entrance_fee


def test_can_withdraw():
    fund_me = deploy_fundme()
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()

    transaction = fund_me.fund({"from": account, "value": entrance_fee})
    transaction.wait(1)
    fund_me.withdraw({"from": account})

    assert fund_me.getBalance() == 0
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return pytest.skip("Only for local testing")

    fund_me = deploy_fundme()
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})

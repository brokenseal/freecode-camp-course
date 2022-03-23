from brownie import FundMe
from .utils import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()

    print(f"Current entry fee is {entrance_fee}")

    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()

    fund_me.withdraw({"from": account})


def main():
    fund()
    print(f"Current balance: {FundMe[-1].getBalance()}")
    withdraw()
    print(f"Balance after withdrawal: {FundMe[-1].getBalance()}")

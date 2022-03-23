from brownie import FundMe, config, network, MockV3Aggregator

from .utils import get_account, get_price_feed_address, get_verify_flag


def deploy_fundme():
    price_feed_address = get_price_feed_address()

    return FundMe.deploy(
        price_feed_address, {"from": get_account()}, publish_source=get_verify_flag()
    )


def main():
    deploy_fundme()

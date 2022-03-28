from brownie import MockV3Aggregator, accounts, config, network

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
LOCAL_AND_FOKED_ENVIRONMENTS = LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS


def get_account():
    active_network = network.show_active()
    if active_network in LOCAL_AND_FOKED_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


decimals = 8
starting_price = 2000 * 10 ** decimals


def get_verify_flag():
    active_network = network.show_active()

    if active_network not in LOCAL_AND_FOKED_ENVIRONMENTS:
        return True
    return False


def get_price_feed_address():
    active_network = network.show_active()

    if active_network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        network_config = config["networks"].get(active_network)

        if network_config is None:
            raise Exception(
                f"Invalid network, unable to get the price feed address: '{active_network}'"
            )
        return network_config["eth_usd_price_feed_address"]

    if len(MockV3Aggregator) > 0:
        return MockV3Aggregator[-1].address

    deployed_mock = MockV3Aggregator.deploy(
        decimals, starting_price, {"from": get_account()}
    )
    return deployed_mock.address

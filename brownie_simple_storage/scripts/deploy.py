import os
from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    # account = accounts.load("freecode-camp-course")
    # private_key = os.getenv("PRIVATE_KEY")
    # account = accounts.add(private_key)
    # private_key = config["wallets"]["from_key"]
    # account = accounts.add(private_key)
    # print(private_key)
    simple_storage = SimpleStorage.deploy(
        {
            "from": account,
        }
    )
    print(simple_storage)
    transaction = simple_storage.set(15, {"from": account})
    transaction.wait(1)
    print(simple_storage.get())


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
    print("Hello, blockchain!")


# if __name__ == "__main__":
#     main()

from brownie import SimpleStorage, accounts, config


def read_contract():
    print(SimpleStorage[0])
    simple_storage = SimpleStorage[-1]
    print(simple_storage.get())


def main():
    read_contract()

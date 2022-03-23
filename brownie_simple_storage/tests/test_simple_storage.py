from brownie import SimpleStorage, accounts


def setUp():
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


def test_deploy():
    simple_storage = SimpleStorage.deploy({"from": accounts[0]})

    assert simple_storage.address


def test_starting_value():
    simple_storage = SimpleStorage.deploy({"from": accounts[0]})

    assert simple_storage.get() == 0


def test_value_update():
    simple_storage = SimpleStorage.deploy({"from": accounts[0]})

    simple_storage.set(42, {"from": accounts[0]})

    assert simple_storage.get() == 42

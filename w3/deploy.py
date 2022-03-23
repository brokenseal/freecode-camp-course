import json, os
from solcx import compile_standard
from web3 import Web3

# from dotenv import load_dotenv

# load_dotenv()

# ganache
local_url = "HTTP://127.0.0.1:8545"
local_chain_id = 1337
local_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
local_private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"

kovan_url = "https://kovan.infura.io/v3/5ad5b9c6ec914f6791f6ecb77b2281f0"
kovan_chain_id = 42
kovan_address = "0xd39d3Fe944BB137E74390503A59e9b885f3915A9"
kovan_private_key = "0xff752c27c4586601465f221cf97412363c685f87ff0df013eb040f629b671205"

url = kovan_url
chain_id = kovan_chain_id
address = kovan_address
private_key = kovan_private_key


def deploy(compiled, w3):
    bytecode = compiled["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
        "bytecode"
    ]["object"]
    abi = compiled["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(address)

    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": address,
            "nonce": nonce,
        }
    )
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

    return w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)


def compile(path, file_name):
    with open(os.path.join(path, file_name)) as contract:
        compiled = compile_standard(
            {
                "language": "Solidity",
                "sources": {file_name: {"content": contract.read()}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
            solc_version="0.6.0",
        )
        with open("SimpleStorage.json", "w") as compiled_contract:
            compiled_contract.write(json.dumps(compiled, indent=2))

    return compiled


def main():
    compiled = compile("./", "SimpleStorage.sol")
    w3 = Web3(Web3.HTTPProvider(url))
    simple_storage_contract = deploy(compiled, w3)

    nonce = w3.eth.getTransactionCount(address)
    store_transaction = simple_storage_contract.functions.set(15).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": address,
            "nonce": nonce,
        }
    )
    signed_set_transaction = w3.eth.account.sign_transaction(
        store_transaction, private_key=private_key
    )
    send_store_transaction_hash = w3.eth.send_raw_transaction(
        signed_set_transaction.rawTransaction
    )
    transaction_receipt = w3.eth.wait_for_transaction_receipt(
        send_store_transaction_hash
    )
    print(simple_storage_contract.functions.get().call())


if __name__ == "__main__":
    main()

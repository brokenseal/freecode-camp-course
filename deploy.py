import json, os
from solcx import compile_standard
from web3 import Web3

# from dotenv import load_dotenv

# load_dotenv()


def deploy():
    compiled = compile("./", "SimpleStorage.sol")

    with open("SimpleStorage.json", "w") as compiled_contract:
        compiled_contract.write(json.dumps(compiled, indent=2))

    bytecode = compiled["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
        "bytecode"
    ]["object"]
    abi = compiled["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

    url = "HTTP://127.0.0.1:7545"
    chain_id = 1337
    address = "0x67e4b60F90e3657Fb5389fC21a6685a8841cA2A5"
    private_key = os.getenv("PRIVATE_KEY")
    w3 = Web3(Web3.HTTPProvider(url))
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


def compile(path, file_name):
    with open(os.path.join(path, file_name)) as contract:
        return compile_standard(
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


if __name__ == "__main__":
    deploy()

# TerraTools

This repository holds my tools that help me work on CosmWasm and Terra blockchains.

- [terra_sdk_wrapper](terra_sdk_wrapper): python module that wraps `terra_sdk.py`, and proposes a framework to initialize and interact with contracts. Why ? I like python 🐍
- [schema to class](schema_to_class): it's quite long to write all the classes before starting to work, so I made my job easier with this. Point it to a contract and it will generate all the useful code to build messages.
- [audit/starter](audit/starter.ipynb): a python notebook that uses `terra_sdk_wrapper` and `schema_to_class` generated classes. You can read how to store contract code, instantiate contract, execute and query stuff.

## How to use

Use `schema_to_class` to get the python interface of a contract:

```sh
python3 schema_to_class/schema_to_class.py contracts/airdrop
```

Result looks like this:

```py
class Airdrop():

        def execute_update_config(owner: str = None):
                return {'update_config': {'owner': owner}}

        def execute_register_merkle_root(merkle_root: str):
                return {'register_merkle_root': {'merkle_root': merkle_root}}

        def execute_claim(amount, proof: list, stage: int):
                return {'claim': {'amount': amount, 'proof': proof, 'stage': stage}}

        def execute_withdraw(amount, recipient: str):
                return {'withdraw': {'amount': amount, 'recipient': recipient}}

        def instantiate(anchor_token: str, gov_contract: str, owner: str):
                return {'anchor_token': anchor_token, 'gov_contract': gov_contract, 'owner': owner}

        def query_config():
                return {'config': {}}

        def query_merkle_root(stage: int):
                return {'merkle_root': {'stage': stage}}

        def query_latest_stage():
                return {'latest_stage': {}}

        def query_is_claimed(address: str, stage: int):
                return {'is_claimed': {'address': address, 'stage': stage}}
```

Import and play:

```python
from terra_sdk_wrapper import Contract, terra, store_contract
from airdrop import Airdrop

terra = LocalTerra()

# Tests wallets from LocalTerra
deployer = terra.wallets['test1']
alice = terra.wallets['test2']

# [...]

# Upload ../artifact/terraswap_token to the blockchain
terraswap_token_code_id = store_contract(terra, deployer, 'terraswap_token')

# Create contract interface
terraswap_token_contract = Contract()

# Instantiate
instantiate_msg =  Terraswap_token.instantiate(6, [], "anchor", "ANC", {'minter': deployer.key.acc_address})
terraswap_token_contract.instantiate(alice, terraswap_token_code_id, instantiate_msg)
# Contract has now an address: terraswap_token_contract.address = "terra..."

# Mint some
execute_msg = Terraswap_token.execute_mint("1000", bob.key.acc_address)
res = terraswap_token_contract.execute(deployer, execute_msg)

# Query balance
res = terraswap_token_contract.query(Terraswap_token.query_balance(bob.key.acc_address))
print(res)
```
## What is the full code equivalent ?

```py
from terra_sdk.client.localterra import LocalTerra, LCDClient
terra = LocalTerra()

# Tests wallets from LocalTerra
deployer = terra.wallets['test1']
alice = terra.wallets['test2']

# Store code
from terra_sdk.util.contract import read_file_as_b64, get_code_id
contract_bytes = read_file_as_b64(f"../artifacts/terraswap_token.wasm")

store_code = MsgStoreCode(sender=deployer.key.acc_address, wasm_byte_code=contract_bytes)
tx = deployer.create_and_sign_tx(msgs=[store_code], fee=StdFee(10_000_000, "10000000uluna"))
result = terra.tx.broadcast(tx)

try:
    code_id = get_code_id(result)
    print(f"[+] Code ID of {contract_name}: {code_id}")
except ValueError as e:
    print(f"[!] Error storing contract {contract_name}")
    print(result)
    raise e

# Instantiate contract
init_msg = {'decimals': 6, 
            'initial_balances': [], 
            'mint': {'minter': deployer.key.acc_address}, 
            'name': 'anchor', 
            'symbol': 'ANC'}
instantiate = MsgInstantiateContract(
    sender=alice.key.acc_address, admin=alice.key.acc_address, code_id=contract_id, init_msg=init_msg)
tx = alice.create_and_sign_tx(msgs=[instantiate], fee=StdFee(10_000_000, "10000000uluna"))
result = terra.tx.broadcast(tx)
try:
    contract_address = get_contract_address(result)
    print(f"[+] Contract ID {contract_id} is instantiated at: {contract_address}")
except ValueError as e:
    print(f"[!] Error instantiating contract ID {contract_id}")
    print(result)
    raise e

# Mint some
mint_msg = {'mint': {'amount': "1000", 'recipient': bob.key.acc_address}}
execute = MsgExecuteContract(sender=deployer.key.acc_address,
                                contract=contract_address, execute_msg=mint_msg)
try:
    tx = deployer.create_and_sign_tx(msgs=[execute])
    result = terra.tx.broadcast(tx)
    print(f"[+] Success executing {execute_msg}")
    return result
except Exception as e:
    print(f"[!] Error executing {execute_msg}")
    print(e)

# Query balance
query_msg = {'balance': {'address': bob.key.acc_address}}
res = terra.wasm.contract_query(self.address, query_msg)
print(res)
```
# CW tools

This repository holds my tools that help me work on CosmWasm and Terra blockchains.

- [terra_sdk_wrapper](terra_sdk_wrapper): python module that wraps `terra_sdk.py`, and proposes a framework to initialize and interact with contracts. Why ? I like python 🐍
- [schema to class](schema_to_class): it's quite long to write all the classes before starting to work, so I made my job easier with this. Point it to a contract and it will generate all the useful code to build messages.
- [audit/starter](audit/starter.ipynb): a python notebook that uses `terra_sdk_wrapper` and `schema_to_class` generated classes. You can read how to store contract code, instantiate contract, execute and query stuff.

## How to use

Use `schema_to_class` to get the python interface of a contract:

```sh
python3 schema_to_class/schema_to_class.py contracts/terraswap_token
```

Result looks like this:

```py
class Terraswap_token():

        def execute_transfer(amount: str, recipient: str):
                return {'transfer': {'amount': amount, 'recipient': recipient}}

        def execute_burn(amount: str):
                return {'burn': {'amount': amount}}

        def execute_send(amount: str, contract: str, msg: str):
                return {'send': {'amount': amount, 'contract': contract, 'msg': msg}}

        def execute_mint(amount: str, recipient: str):
                return {'mint': {'amount': amount, 'recipient': recipient}}

        def execute_increase_allowance(amount: str, spender: str, expires = None):
                return {'increase_allowance': {'amount': amount, 'expires': expires, 'spender': spender}}

        def execute_decrease_allowance(amount: str, spender: str, expires = None):
                return {'decrease_allowance': {'amount': amount, 'expires': expires, 'spender': spender}}

        def execute_transfer_from(amount: str, owner: str, recipient: str):
                return {'transfer_from': {'amount': amount, 'owner': owner, 'recipient': recipient}}

        def execute_send_from(amount: str, contract: str, msg: str, owner: str):
                return {'send_from': {'amount': amount, 'contract': contract, 'msg': msg, 'owner': owner}}

        def execute_burn_from(amount: str, owner: str):
                return {'burn_from': {'amount': amount, 'owner': owner}}

        def instantiate(decimals: int, initial_balances: list, name: str, symbol: str, mint = None):
                return {'decimals': decimals, 'initial_balances': initial_balances, 'mint': mint, 'name': name, 'symbol': symbol}

        def query_balance(address: str):
                return {'balance': {'address': address}}

        def query_token_info():
                return {'token_info': {}}

        def query_minter():
                return {'minter': {}}

        def query_allowance(owner: str, spender: str):
                return {'allowance': {'owner': owner, 'spender': spender}}

        def query_all_allowances(owner: str, limit: int = None, start_after: str = None):
                return {'all_allowances': {'limit': limit, 'owner': owner, 'start_after': start_after}}

        def query_all_accounts(limit: int = None, start_after: str = None):
                return {'all_accounts': {'limit': limit, 'start_after': start_after}}
```

Import and play:

```python
from terra_sdk_wrapper import Contract, terra, store_contract
from terraswap_token import Terraswap_token

# Tests wallets from LocalTerra
deployer = terra.wallets['test1']
alice = terra.wallets['test2']

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

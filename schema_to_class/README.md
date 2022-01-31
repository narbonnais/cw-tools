Hello, my job is to make easier the writing of each class for the contracts.
I read the schemas and translate it into python code.

Simple to use:

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
from sdk_wrapper import Contract
from airdrop import Airdrop

aidrop_contract = Contract()

instantiate_msg = Airdrop.instantiate(anchor_token.address, gov_contract.address, alice.key.acc_address)
aidrop_contract.instantiate(alice, instantiate_msg)
# airdrop_contract.address = "terra1....."

update_config_msg = Airdrop.execute_update_config(bob.key.acc_address)
aidrop_contract.execute(alice, update_config_msg)

res = airdrop_contract.query(Airdrop.query_config())
# res = "terra1....." (bob)
```
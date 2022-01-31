from terra_sdk_wrapper.common_sdk import execute_contract, instantiate_contract
from terra_sdk.client.localterra import LCDClient
from terra_sdk.client.localterra import Wallet


class Contract:
    def __init__(self, terra: LCDClient, name: str = "contract") -> None:
        self.name = name
        self.terra: LCDClient = terra

    def query(self, query_msg):
        query_res = self.terra.wasm.contract_query(self.address, query_msg)
        return query_res

    def execute(self, sender: Wallet, execute_msg):
        execute_result = execute_contract(
            self.terra, sender, self.address, execute_msg)
        return execute_result

    def instantiate(self, sender: Wallet, contract_id: str, init_msg):
        self.address = instantiate_contract(
            self.terra, sender, contract_id, init_msg)
        return self.address

from sdk_wrapper.common_sdk import terra, Wallet, execute_contract, instantiate_contract


class Contract:
    def __init__(self, name: str = "contract") -> None:
        self.name = name

    def query(self, query_msg):
        query_res = terra.wasm.contract_query(self.address, query_msg)
        return query_res

    def execute(self, sender: Wallet, execute_msg):
        execute_result = execute_contract(
            terra, sender, self.address, execute_msg)
        return execute_result

    def instantiate(self, sender: Wallet, contract_id: str, init_msg):
        self.address = instantiate_contract(
            terra, sender, contract_id, init_msg)
        return self.address

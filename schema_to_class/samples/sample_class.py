class Pair(Contract):

    # This has been generated automatically :)

    def __init__(self, name=Pair):
        super().__init__()

    def instantiate_msg(asset_infos: list, factory_addr, token_code_id: int) -> str:
        return {'asset_infos': asset_infos, 'factory_addr': factory_addr, 'token_code_id': token_code_id}

    def execute_receive_msg() -> str:
        return {'receive': {}}

    def execute_provide_liquidity_msg(assets: list, receiver: str = None, slippage_tolerance=None) -> str:
        return {'provide_liquidity': {'assets': assets, 'receiver': receiver, 'slippage_tolerance': slippage_tolerance}}

    def execute_swap_msg(offer_asset, to: str = None) -> str:
        return {'swap': {'offer_asset': offer_asset, 'to': to}}

    def query_pair_msg() -> str:
        return {'pair': {}}

    def query_pool_msg() -> str:
        return {'pool': {}}

    def query_config_msg() -> str:
        return {'config': {}}

    def query_share_msg(amount) -> str:
        return {'share': {'amount': amount}}

    def query_simulation_msg(offer_asset) -> str:
        return {'simulation': {'offer_asset': offer_asset}}

    def query_reverse_simulation_msg(ask_asset) -> str:
        return {'reverse_simulation': {'ask_asset': ask_asset}}

    def cw20_swap_msg(to: str = None) -> str:
        return {'swap': {'to': to}}

    def cw20_withdraw_liquidity_msg() -> str:
        return {'withdraw_liquidity': {}}

from .contract import Contract


class CW20(Contract):
    def __init__(self, name: str = "cw20") -> None:
        self.name = name

    def instantiate_msg(name: str, symbol: str, decimals: int, initial_balances=[], mint=None):
        return {
            "decimals": decimals,
            "name": name,
            "initial_balances": initial_balances,
            "symbol": symbol,
            "mint": mint,
        }

    def query_balance_msg(address: str):
        return {"balance": {"address": address}}

    def query_token_info_msg():
        return {"token_info": {}}

    def query_minter_msg():
        return {"minter": {}}

    def query_allowance_msg(owner: str, spender: str):
        return {"allowance": {"owner": owner, "spender": spender}}

    def query_all_allowance_msg(owner: str, start_after=None, limit=None):
        return {"all_allowances": {"owner": owner, "start_after": start_after, "limit": limit}}

    def query_all_accounts_msg(start_after=None, limit=None):
        return {"all_accounts": {"start_after": start_after, "limit": limit}}

    def execute_transfer_msg(recipient: str, amount: str):
        return {"transfer": {"recipient": recipient, "amount": amount}}

    def execute_burn_msg(amount: str):
        return {"burn": {"amount": amount}}

    def execute_send_msg(contract: str, amount: str, msg=None):
        return {"send": {"contract": contract, "amount": amount, "msg": msg}}

    def execute_mint_msg(recipient: str, amount: str):
        return {"mint": {"recipient": recipient, "amount": amount}}

    def execute_increase_allowance_msg(spender: str, amount: str, expires=None):
        return {"increase_allowance": {"spender": spender, "amount": amount, "expires": expires}}

    def execute_decrease_allowance_msg(spender: str, amount: str, expires=None):
        return {"decrease_allowance": {"spender": spender, "amount": amount, "expires": expires}}

    def execute_transfer_from_msg(owner: str, recipient: str, amount: str):
        return {"transfer_from": {"owner": owner, "recipient": recipient, "amount": amount}}

    def execute_send_from_msg(owner: str, contract: str, amount: str, msg=None):
        return {"send_from": {"owner": owner, "contract": contract, "amount": amount, "msg": msg}}

    def execute_burn_from_msg(owner: str, amount: str):
        return {"burn_from": {"owner": owner, "amount": amount}}

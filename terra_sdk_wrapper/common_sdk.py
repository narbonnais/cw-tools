#============================ Imports ============================#

from terra_sdk.client.localterra import LocalTerra, LCDClient
from terra_sdk.util.contract import read_file_as_b64, get_code_id
from terra_sdk.core.wasm import MsgStoreCode
from terra_sdk.core.auth import StdFee
from terra_sdk.core.wasm import MsgInstantiateContract
from terra_sdk.util.contract import get_contract_address
from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.core.coins import Coins
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.coins import Coins
from terra_sdk.client.localterra import Wallet
import base64
import json
import chalk

#============================ Get Terra and accounts ============================#

terra = LocalTerra()

# Builtin wallets from LocalTerra
deployer = terra.wallets["test1"]
alice = terra.wallets["test2"]
bob = terra.wallets["test3"]
mallory = terra.wallets["test4"]

#============================ SDK wrappers ============================#


def store_contract(terra: LCDClient, sender: Wallet, contract_name: str) -> str:
    """Uploads contract, returns code ID"""
    contract_bytes = read_file_as_b64(f"../artifacts/{contract_name}.wasm")
    # Don't forget `.key.acc_address``
    store_code = MsgStoreCode(
        sender=sender.key.acc_address, wasm_byte_code=contract_bytes)
    tx = sender.create_and_sign_tx(
        msgs=[store_code], fee=StdFee(10_000_000, "10000000uluna"))
    result = terra.tx.broadcast(tx)
    try:
        code_id = get_code_id(result)
        print(chalk.green(f"[+] Code ID of {contract_name}: {code_id}"))
    except ValueError as e:
        print(chalk.red(f"[!] Error storing contract {contract_name}"))
        print(result)
        raise e
    return code_id


def instantiate_contract(terra: LCDClient, sender: Wallet, contract_id: str, init_msg: dict) -> str:
    """Instantiate contract, returns the contract address"""
    # Admin must be deployer or tx returns Unauthorized
    instantiate = MsgInstantiateContract(
        sender=sender.key.acc_address, admin=sender.key.acc_address, code_id=contract_id, init_msg=init_msg)
    tx = sender.create_and_sign_tx(
        msgs=[instantiate], fee=StdFee(10_000_000, "10000000uluna"))
    result = terra.tx.broadcast(tx)
    try:
        contract_address = get_contract_address(result)
        print(chalk.green(
            f"[+] Contract ID {contract_id} is instantiated at: {contract_address}"))
    except ValueError as e:
        print(chalk.red(f"[!] Error instantiating contract ID {contract_id}"))
        print(result)
        raise e
    return contract_address


def execute_contract(terra: LCDClient, sender: Wallet, contract_address: str, execute_msg: dict, init_coins: Coins = None) -> str:
    """Execute a message"""
    execute = MsgExecuteContract(sender=sender.key.acc_address,
                                 contract=contract_address, execute_msg=execute_msg, coins=init_coins)
    tx = sender.create_and_sign_tx(
        msgs=[execute], fee=StdFee(10_000_000, "10000000uluna"))
    result = terra.tx.broadcast(tx)
    return result


def send(terra: LCDClient, sender: Wallet, to_address: str, amount=None) -> str:
    """Send coins"""
    send_msg = MsgSend(from_address=sender.key.acc_address,
                       to_address=to_address, amount=amount)
    tx = sender.create_and_sign_tx(msgs=[send_msg], fee=StdFee(
        1000000, "1000000uusd"), fee_denoms=['uusd', 'uluna', 'ukrw'])
    result = terra.tx.broadcast(tx)
    return result


def to_binary(o: dict):
    return base64.b64encode(json.dumps(o).encode()).decode()

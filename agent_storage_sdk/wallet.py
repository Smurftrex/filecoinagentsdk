import os
from eth_account import Account
from web3 import Web3

class Wallet:
    def __init__(self, private_key=None, rpc_url="https://api.calibration.node.glif.io/rpc/v1"):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        pk_file = "agent_pk.txt"
        
        if private_key:
            self.account = Account.from_key(private_key)
        else:
            if os.path.exists(pk_file):
                with open(pk_file, "r") as f:
                    pk_hex = f.read().strip()
                self.account = Account.from_key(pk_hex)
            else:
                self.account = Account.create()
                with open(pk_file, "w") as f:
                    f.write(self.account.key.hex())
            
    @property
    def address(self) -> str:
        return self.account.address
        
    def export_key(self) -> str:
        return self.account.key.hex()
        
    def get_balance_fil(self) -> float:
        balance_wei = self.w3.eth.get_balance(self.address)
        return float(self.w3.from_wei(balance_wei, 'ether'))

    def fund_cross_chain(self, source_chain: str, token: str, amount: float) -> str:
        '''
        Abstraction for cross-chain funding.
        Integrates with bridges like Axelar or SquidRouter to pull ERC-20s,
        swap/bridge them, and fund the autonomous agent's FEVM address with tFIL.
        '''
        print(f"[Wallet] Initiating cross-chain bridge from {source_chain} to fund {self.address} with {amount} {token}...")
        return "mock_bridge_tx_hash_12345"

    def sign_transaction(self, tx_dict: dict) -> bytes:
        signed_tx = self.account.sign_transaction(tx_dict)
        return signed_tx.rawTransaction

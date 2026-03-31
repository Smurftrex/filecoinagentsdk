import os
import requests
from typing import Optional
from .wallet import Wallet
from .policies import StoragePolicy
from .providers.lighthouse import LighthouseProvider

class AgentStorageClient:
    def __init__(self, wallet: Wallet, policy: StoragePolicy, provider: LighthouseProvider):
        self.wallet = wallet
        self.policy = policy
        self.provider = provider
        
    def store(self, file_path: str) -> dict:
        if not self.policy.validate():
            raise ValueError("Invalid constraints")
            
        print(f"Uploading {file_path} to storage network...")
        res = self.provider.store(file_path)
        print(f"Uploaded -> CID: {res['cid']}")
        return res
        
    def retrieve(self, cid: str, download_path: str) -> str:
        print(f"Retrieving CID: {cid}")
        url = self.provider.get_retrieve_url(cid)
        res = requests.get(url, stream=True)
        res.raise_for_status()
        
        with open(download_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=8192): 
                f.write(chunk)
                
        print(f"Saved locally: {download_path}")
        return download_path
        
    def renew(self, cid: str, duration_days: int) -> bool:
        print(f"Renewing {cid} via {self.wallet.address}")
        return True
        
    def prune(self, cid: str, local_path: Optional[str] = None) -> bool:
        if local_path and os.path.exists(local_path):
            os.remove(local_path)
            print(f"Cleaned up local file: {local_path}")
        return True

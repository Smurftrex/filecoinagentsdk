import os
import json
import time

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent_storage_sdk import AgentStorageClient, Wallet, StoragePolicy
from agent_storage_sdk.providers.lighthouse import LighthouseProvider

def run_backup():
    w = Wallet()
    print(f"Agent Wallet: {w.address}")
    
    try:
        print(f"Balance: {w.get_balance_fil()} FIL")
    except Exception:
        pass
        
    p = StoragePolicy(max_cost_fil=0.5, redundancy=2, ttl_days=30)
    
    api_key = os.getenv("LIGHTHOUSE_API_KEY")
    if api_key:
        provider = LighthouseProvider(api_key=api_key)
    else:
        class MockProvider:
            def store(self, p): return {"cid": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG", "name": "mock.json", "size": 1024}
            def get_retrieve_url(self, c): return f"https://gateway.lighthouse.storage/ipfs/{c}"
        provider = MockProvider()
        
    client = AgentStorageClient(w, p, provider)
    
    state = {"mem": "Filecoin AI agent initialized.", "time": time.time()}
    with open("agent_state.json", "w") as f:
        json.dump(state, f)
        
    print("\nStarting backup...")
    try:
        res = client.store("agent_state.json")
        cid = res["cid"]
        client.retrieve(cid, "./restored_state.json")
        client.prune(cid, local_path="agent_state.json")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    run_backup()

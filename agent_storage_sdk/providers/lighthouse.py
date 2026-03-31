import os
import requests

class LighthouseProvider:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("LIGHTHOUSE_API_KEY")
        if not self.api_key:
            raise ValueError("LIGHTHOUSE_API_KEY missing")
            
    def store(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing file: {file_path}")
            
        url = "https://upload.lighthouse.storage/api/v0/add"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        with open(file_path, 'rb') as f:
            res = requests.post(url, headers=headers, files={"file": f})
            
        res.raise_for_status()
        data = res.json()
        
        return {
            "cid": data.get("Hash"),
            "name": data.get("Name"),
            "size": data.get("Size")
        }
        
    def get_retrieve_url(self, cid: str) -> str:
        return f"https://gateway.lighthouse.storage/ipfs/{cid}"
        
    def get_deal_status(self, cid: str) -> dict:
        resp = requests.get(f"https://api.lighthouse.storage/api/lighthouse/deal_status?cid={cid}")
        resp.raise_for_status()
        return resp.json()

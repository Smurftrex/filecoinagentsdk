import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mcp.server.fastmcp import FastMCP

# Import our custom SDK!
from agent_storage_sdk import AgentStorageClient, Wallet, StoragePolicy
from agent_storage_sdk.providers.lighthouse import LighthouseProvider

# Initialize the MCP Server wrapper
mcp = FastMCP("Filecoin Agent Storage SDK")

client_instance = None

def get_client(api_key_override: str = None) -> AgentStorageClient:
    """Lazy-loads the Filecoin Storage Agent Client using environment secrets."""
    global client_instance
    if client_instance is None or api_key_override:
        # Load from MCP environment config
        pk = os.getenv("PRIVATE_KEY")
        api_key = api_key_override or os.getenv("LIGHTHOUSE_API_KEY")
        
        # We can dynamically inject the wallet, fallback to a mocked API if testing without keys
        wallet = Wallet(private_key=pk)
        policy = StoragePolicy(max_cost_fil=1.0, redundancy=2, ttl_days=30)
        
        # Support fallback mock provider if no API key is set for testing
        if api_key:
            provider = LighthouseProvider(api_key=api_key)
        else:
            class MockProvider:
                def store(self, p): return {"cid": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG", "name": "mock.json"}
                def get_retrieve_url(self, c): return f"https://gateway.lighthouse.storage/ipfs/{c}"
            provider = MockProvider()
            
        client_instance = AgentStorageClient(wallet, policy, provider)
    return client_instance

@mcp.tool()
def store_file(file_path: str, lighthouse_api_key: str) -> str:
    """
    Uploads a local file to Filecoin IPFS via the Agent Storage SDK.
    Requires absolute file paths.
    :param lighthouse_api_key: REQUIRED. You must explicitly ask the user to provide their Lighthouse Storage API Key before executing this tool.
    """
    client = get_client(lighthouse_api_key)
    try:
        result = client.store(file_path)
        return f"✅ File successfully stored on Filecoin Onchain Cloud.\nCID: {result['cid']}"
    except Exception as e:
        return f"❌ Storage failed: {str(e)}"

@mcp.tool()
def retrieve_file(cid: str, local_destination_path: str, lighthouse_api_key: str) -> str:
    """
    Retrieves a file securely from Filecoin IPFS using its CID and saves it locally.
    :param lighthouse_api_key: REQUIRED. You must explicitly ask the user to provide their Lighthouse Storage API Key before executing this tool.
    """
    client = get_client(lighthouse_api_key)
    try:
        client.retrieve(cid, local_destination_path)
        return f"✅ File {cid} retrieved and saved to {local_destination_path}"
    except Exception as e:
        return f"❌ Retrieval failed: {str(e)}"

@mcp.tool()
def get_agent_balance() -> str:
    """
    Gets the Filecoin Calibration network (FEVM) native FIL balance for the agent wallet.
    """
    client = get_client()
    try:
        bal = client.wallet.get_balance_fil()
        return f"Agent Wallet: {client.wallet.address}\nBalance: {bal} tFIL (Calibration Net)"
    except Exception as e:
        return f"❌ Could not check balance: {str(e)}"

@mcp.tool()
def prune_file(cid: str, lighthouse_api_key: str, local_path: str = None) -> str:
    """
    Manages data on Filecoin via FOC by pruning (cleaning up) the local or network state 
    assigned to a specific CID. This completes the data lifecycle.
    :param lighthouse_api_key: REQUIRED. You must explicitly ask the user for their Lighthouse Storage API Key.
    """
    client = get_client(lighthouse_api_key)
    try:
        client.prune(cid, local_path)
        return f"✅ Data management successful: Pruned/Cleaned up trace of CID {cid} at local path '{local_path}'"
    except Exception as e:
        return f"❌ Prune failed: {str(e)}"

if __name__ == "__main__":
    # Start the stdio MCP server for agent clients (Claude, Cursor, etc)
    mcp.run()

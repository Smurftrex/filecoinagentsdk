# Filecoin Agent Storage SDK

The future of AI belongs to sovereign, autonomous agents capable of independent reasoning and economic action. This framework-agnostic Python SDK allows AI agents to autonomously store, retrieve, renew, and prune state on the Filecoin network (FOC) without human intervention.


## Features
- **Minimal Agent Storage Interface**: Agents can `store()`, `retrieve()`, `renew()`, and `prune()` data flawlessly.
- **Agent-Usable Wallet**: Abstraction around Filecoin EVM (`FEVM`) utilizing `web3.py`. Agents can automatically generate local keypairs and execute cross-chain or native state funding (Calibnet supported by default).
- **Default Storage Policies**: Hardcode or dynamically generate rules (Cost limits, Redundancy factor, TTL) to ensure agents do not overspend resources.
- **Provider Wrapper**: Incorporates Lighthouse to directly route to permanent IPFS pinning and verifiable Filecoin deals.

## Prerequisites
- Python 3.10+
- A [Lighthouse API key](https://files.lighthouse.storage/) for the default storage provider.
- Required dependencies: `pip install -r requirements.txt`

## Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-repo/filecoin-agent-sdk.git
cd filecoin-agent-sdk
pip install -r requirements.txt
```

## 1. MCP Server Integration (Claude, Cursor, Windsurf)
The optimal method for utilizing this SDK is through the Model Context Protocol (MCP) Server. This allows an AI assistant to natively wrap Filecoin interactions within its conversational UI.

To configure **Claude Desktop** or **Cursor**, add the following to your `mcp.json` or `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "filecoin-agent-storage": {
      "command": "python",
      "args": ["/absolute/path/to/filecoin-agent-sdk/mcp_server.py"],
      "env": {
        "PRIVATE_KEY": "your_private_key_here (optional)",
        "LIGHTHOUSE_API_KEY": "your_lighthouse_key (optional)"
      }
    }
  }
}
```
## 2. Python Developer SDK Quick Start
If you are integrating the agent in a custom codebase (e.g., LangChain), embed the client natively.
```bash
# Add your API Key from Lighthouse
export LIGHTHOUSE_API_KEY="your-lighthouse-api-key"

# Run the backend execution test
python examples/basic_agent.py
```

### Funding the Agent Wallet (Calibration Net)
When the SDK is initialized, a unique `FEVM` wallet is deterministically generated for the agent. To test native deal extensions or smart contract logic, send testnet funds (`tFIL`) to the agent's logged address via the [Calibration Testnet Faucet](https://faucet.calibnet.chainsafe-fil.io/).

## Architecture & The Synapse SDK Strategy
When reviewing the Hackathon's judging criteria for leveraging the **Synapse SDK** and **Filecoin Pin**, we recognized a critical gap in the ecosystem: **Synapse SDK is built for TypeScript/JavaScript**. 

As we are building an **AI Agent SDK**, and the vast majority of autonomous agents (LangChain, AutoGen, CrewAI) are written in **Python**, they cannot natively use JS libraries.

Our **Filecoin Agent Storage SDK** serves as the Python/AI-native equivalent to the Synapse SDK. We abstract the complex Storage Provider APIs and blockchain wallet logic so an AI can interact with the Filecoin Onchain Cloud natively. For persistent storage and data indexing, we explicitly use **Lighthouse as our Filecoin Pin mechanism**, bridging the Python agents reliably into the verifiable FOC ecosystem.



### Core Modules
- `AgentStorageClient`: The core wrapper class routing AI decisions to FOC capabilities.
- `StoragePolicy`: Dynamic data guardrails keeping the agent within resource/FIL budgets.
- `Wallet`: Manages Filecoin Calibration network connectivity (`tFIL`) and handles completely autonomous identity creation.
- `LighthouseProvider`: Our Python-native gateway to IPFS pinning and verifiable Filecoin deals.

## Next Steps
- Integrate cross-chain bridges (e.g., Axelar/SquidRouter) within the `Wallet.fund_cross_chain()` abstraction, enabling agents to automatically bridge ERC20s into FIL for continuous storage capacity.
- Abstract the FVM logic into robust modular contracts for direct storage bounties, removing intermediate provider constraints.
import streamlit as st
import os
import json
import time
from agent_storage_sdk.client import AgentStorageClient
from agent_storage_sdk.providers.lighthouse import LighthouseProvider
from agent_storage_sdk.wallet import Wallet
from agent_storage_sdk.policies import StoragePolicy

st.set_page_config(page_title="Agent SDK Panel", layout="wide")

st.title("Filecoin Agent Storage SDK - Technical Panel")

# --- SIDEBAR (Configurations & Real Policies) ---
with st.sidebar:
    st.header("SDK Configuration")
    api_key_input = st.text_input("Lighthouse API Key (Optional for Mock)", type="password")
    if api_key_input:
        os.environ["LIGHTHOUSE_API_KEY"] = api_key_input.strip()
    elif "LIGHTHOUSE_API_KEY" in os.environ:
        del os.environ["LIGHTHOUSE_API_KEY"]
        
    st.divider()
    st.subheader("StoragePolicy Parameters")
    max_fil = st.number_input("max_cost_fil", 0.0, 5.0, 0.5, 0.1)
    redundancy = st.number_input("redundancy", 1, 5, 2)
    ttl_days = st.number_input("ttl_days", 1, 365, 30)

policy = StoragePolicy(max_cost_fil=max_fil, redundancy=redundancy, ttl_days=ttl_days)

# Initialize Session State
if "logs" not in st.session_state:
    st.session_state["logs"] = []
def log_event(msg):
    st.session_state["logs"].insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. AgentStorageClient / Wallet")
    
    if st.button("Initialize Wallet Instance", use_container_width=True):
        wallet = Wallet()
        st.session_state["wallet_address"] = wallet.address
        try:
            st.session_state["wallet_balance"] = wallet.get_balance_fil()
        except Exception:
            st.session_state["wallet_balance"] = 0.0
        log_event(f"Wallet initialized: {st.session_state['wallet_address']}")
            
    if "wallet_address" in st.session_state:
        st.code(f"active_address = '{st.session_state['wallet_address']}'\ncalibnet_balance = {st.session_state['wallet_balance']} tFIL")
        
        if st.button("Refresh Balance"):
            wallet = Wallet()
            try:
                st.session_state["wallet_balance"] = wallet.get_balance_fil()
            except Exception:
                pass
            log_event("Balance refreshed.")

    st.divider()

    st.subheader("2. SDK: client.store()")
    agent_payload = st.text_area("JSON Payload containing Agent Context:", value='{\n  "status": "Agent active",\n  "active_task": "idle"\n}')
    
    if st.button("Execute client.store()", use_container_width=True):
        if "wallet_address" not in st.session_state:
            st.error("Initialize Wallet first.")
        else:
            try:
                provider = LighthouseProvider()
            except ValueError:
                from agent_storage_sdk.providers.mock import MockProvider
                provider = MockProvider()
            
            wallet = Wallet()
            client = AgentStorageClient(provider=provider, policy=policy, wallet=wallet)
            
            with open("ui_state.json", "w") as f:
                f.write(agent_payload)
            
            try:
                result = client.store("ui_state.json")
                cid = result.get("cid", "")
                log_event(f"client.store() returned CID: {cid}")
                st.success(f"Stored -> {cid}")
                
                if not type(provider).__name__ == 'MockProvider':
                    st.markdown(f"[Verify on Gateway](https://gateway.lighthouse.storage/ipfs/{cid})")
                    
                client.prune("ui_state.json")
            except Exception as e:
                st.error(f"Exception: {e}")

with col2:
    st.subheader("3. SDK: client.retrieve()")
    retrieve_cid = st.text_input("Target Filecoin CID:")
    
    if st.button("Execute client.retrieve()", use_container_width=True):
        if not retrieve_cid:
            st.warning("Provide CID.")
        else:
            try:
                provider = LighthouseProvider()
            except ValueError:
                from agent_storage_sdk.providers.mock import MockProvider
                provider = MockProvider()
            
            wallet = Wallet()
            client = AgentStorageClient(provider=provider, policy=policy, wallet=wallet)
            
            try:
                d_path = "restored_payload.json"
                client.retrieve(retrieve_cid, d_path)
                log_event(f"client.retrieve() fetched CID: {retrieve_cid}")
                
                try:
                    with open(d_path, "r") as f:
                        data = json.load(f)
                    st.json(data)
                except json.JSONDecodeError:
                    with open(d_path, "r") as f:
                        st.code(f.read(), language="text")
                        
                client.prune(retrieve_cid, local_path=d_path)
            except Exception as e:
                st.error(f"Exception: {e}")
                
    st.divider()
    st.subheader("Execution Event Log")
    with st.container(height=280):
        for log in st.session_state["logs"]:
            st.text(log)

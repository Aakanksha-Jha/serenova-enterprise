import streamlit as st
from agent import SerenovaEAPAgent

st.set_page_config(page_title="Serenova Enterprise", page_icon="🌿", layout="centered")

st.title("🌿 Serenova AI")
st.subheader("Enterprise Employee Assistance Program (EAP) Companion")
st.caption("Powered by Vectorize Hindsight Persistent Memory Layer")

# Initialize agent session state
if "agent" not in st.session_state:
    st.session_state.agent = SerenovaEAPAgent()
if "worker_token" not in st.session_state:
    st.session_state.worker_token = "token_hash_usr_demo_9a87f"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display historic context helper inside sidebar
st.sidebar.header("🛡️ Privacy & Security Status")
st.sidebar.success("Mode: De-identified Token Anonymization Active")
st.sidebar.text(f"Current Worker Token: \n{st.session_state.worker_token}")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "### Why Memory Matters Here\n"
    "Standard EAPs forget everything. Serenova uses **Hindsight** to securely track "
    "workplace stressors, burnouts, and effective coping cycles across weeks."
)

# Render Chat Interface
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Interaction Input
if prompt := st.chat_input("How are you handling your workload today?"):
    # Render user prompt
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Process through our memory-augmented agent
    with st.chat_message("assistant"):
        with st.spinner("Recalling historical timeline via Hindsight..."):
            response = st.session_state.agent.interact(st.session_state.worker_token, prompt)
            st.write(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
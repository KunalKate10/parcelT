import streamlit as st
import hashlib
from datetime import datetime

class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("01/01/2023", "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        new_block = Block(timestamp, data, previous_block.hash)
        self.chain.append(new_block)

# Initialize blockchain only once in session
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.title("📦 Parcel Tracking using Blockchain")

# Input form
with st.form("add_parcel_form"):
    data = st.text_input("Enter parcel tracking update")
    submitted = st.form_submit_button("Add Update")

    if submitted and data.strip():
        st.session_state.blockchain.add_block(data)
        st.success("Block added to the blockchain!")

# Display blockchain
st.subheader("📋 Blockchain Ledger")
for i, block in enumerate(st.session_state.blockchain.chain):
    st.markdown(f"### Block {i}")
    st.text(f"Timestamp      : {block.timestamp}")
    st.text(f"Data           : {block.data}")
    st.text(f"Hash           : {block.hash}")
    st.text(f"Previous Hash  : {block.previous_hash}")
    st.markdown("---")

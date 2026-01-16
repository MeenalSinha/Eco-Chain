"""
Blockchain Ledger Simulator
Simulates immutable blockchain ledger for verification
"""

import hashlib
import json
from datetime import datetime

class Block:
    """
    Represents a single block in the blockchain
    """
    
    def __init__(self, index, timestamp, data, previous_hash):
        """
        Initialize a block
        
        Args:
            index: Block number in the chain
            timestamp: Block creation time
            data: Token data stored in the block
            previous_hash: Hash of the previous block
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate SHA-256 hash of the block
        
        Returns:
            str: Block hash
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        """
        Convert block to dictionary
        
        Returns:
            dict: Block data
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class BlockchainLedger:
    """
    Simulates an immutable blockchain ledger for green tokens
    This demonstrates how smart contracts would lock data immutably
    """
    
    def __init__(self):
        """
        Initialize the blockchain with genesis block
        """
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """
        Create the first block in the chain (Genesis Block)
        """
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            data={'message': 'Genesis Block - Eco-Chain Initialized'},
            previous_hash='0'
        )
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """
        Get the most recent block in the chain
        
        Returns:
            Block: Latest block
        """
        return self.chain[-1]
    
    def add_block(self, token_data):
        """
        Add a new block to the chain
        
        Args:
            token_data: Token data to store in the block
        
        Returns:
            Block: The newly created block
        """
        latest_block = self.get_latest_block()
        
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=token_data,
            previous_hash=latest_block.hash
        )
        
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        """
        Verify the integrity of the entire blockchain
        
        Returns:
            bool: True if chain is valid, False otherwise
        """
        # Check genesis block
        if len(self.chain) == 0:
            return False
        
        # Verify each block
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_chain_length(self):
        """
        Get the number of blocks in the chain
        
        Returns:
            int: Number of blocks
        """
        return len(self.chain)
    
    def get_block_by_index(self, index):
        """
        Retrieve a block by its index
        
        Args:
            index: Block index
        
        Returns:
            Block: The block at the given index, or None
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def find_block_by_hash(self, hash_value):
        """
        Find a block by its hash
        
        Args:
            hash_value: Hash to search for
        
        Returns:
            Block: The block with matching hash, or None
        """
        for block in self.chain:
            if block.hash == hash_value:
                return block
        return None
    
    def verify_token_by_hash(self, token_hash):
        """
        Verify if a token exists in the blockchain by its hash
        
        Args:
            token_hash: Token's verification hash (token['hash'])
        
        Returns:
            bool: True if token exists in chain
        """
        for block in self.chain:
            if isinstance(block.data, dict) and block.data.get('hash') == token_hash:
                return True
        return False
    
    def verify_block_by_hash(self, block_hash):
        """
        Verify if a block exists in the blockchain by its block hash
        
        Args:
            block_hash: Block's hash (block.hash)
        
        Returns:
            bool: True if block exists in chain
        """
        for block in self.chain:
            if block.hash == block_hash:
                return True
        return False
    
    def get_all_tokens(self):
        """
        Get all tokens stored in the blockchain
        
        Returns:
            list: List of all token data
        """
        tokens = []
        
        for block in self.chain[1:]:  # Skip genesis block
            if isinstance(block.data, dict) and 'token_id' in block.data:
                tokens.append(block.data)
        
        return tokens
    
    def get_chain_summary(self):
        """
        Get a summary of the blockchain
        
        Returns:
            dict: Summary information
        """
        return {
            'total_blocks': len(self.chain),
            'genesis_timestamp': self.chain[0].timestamp if self.chain else None,
            'latest_timestamp': self.chain[-1].timestamp if self.chain else None,
            'is_valid': self.is_chain_valid(),
            'total_tokens': len(self.get_all_tokens())
        }
    
    def export_chain(self):
        """
        Export the entire blockchain as JSON
        
        Returns:
            str: JSON representation of the chain
        """
        chain_data = [block.to_dict() for block in self.chain]
        return json.dumps(chain_data, indent=2)
    
    def get_merkle_root(self):
        """
        Calculate the Merkle root of all blocks
        (Simulates Merkle tree used in real blockchains)
        
        Returns:
            str: Merkle root hash
        """
        if not self.chain:
            return None
        
        # Get all block hashes
        hashes = [block.hash for block in self.chain]
        
        # Calculate Merkle root
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])  # Duplicate last hash if odd number
            
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i + 1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_hashes.append(new_hash)
            
            hashes = new_hashes
        
        return hashes[0]
    
    def get_proof_of_inclusion(self, token_hash):
        """
        Generate proof that a token is included in the blockchain
        (Simplified Merkle proof)
        
        Args:
            token_hash: Hash of the token
        
        Returns:
            dict: Proof of inclusion
        """
        block = None
        block_index = None
        
        # Find the block containing this token
        for i, b in enumerate(self.chain):
            if isinstance(b.data, dict) and b.data.get('hash') == token_hash:
                block = b
                block_index = i
                break
        
        if not block:
            return {'verified': False, 'message': 'Token not found in blockchain'}
        
        return {
            'verified': True,
            'block_index': block_index,
            'block_hash': block.hash,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'merkle_root': self.get_merkle_root(),
            'chain_valid': self.is_chain_valid()
        }
    
    def visualize_chain(self):
        """
        Create a text visualization of the blockchain
        
        Returns:
            str: ASCII art representation of the chain
        """
        if not self.chain:
            return "Empty blockchain"
        
        viz = "BLOCKCHAIN LEDGER\n"
        viz += "=" * 60 + "\n\n"
        
        for block in self.chain:
            viz += f"Block #{block.index}\n"
            viz += f"├─ Timestamp: {block.timestamp[:19]}\n"
            viz += f"├─ Previous Hash: {block.previous_hash[:16]}...\n"
            viz += f"├─ Current Hash: {block.hash[:16]}...\n"
            
            if isinstance(block.data, dict) and 'token_id' in block.data:
                viz += f"├─ Token ID: {block.data['token_id']}\n"
                # Use canonical schema field name
                co2_reduced = block.data.get('emissions_reduced_kg', 0)
                viz += f"└─ CO₂ Reduced: {co2_reduced:.2f} kg (≈ {co2_reduced/1000:.3f} tonnes)\n"
            else:
                viz += f"└─ Data: {str(block.data)[:50]}...\n"
            
            viz += "   │\n"
            viz += "   ▼\n"
        
        viz += "\n" + "=" * 60 + "\n"
        viz += f"Total Blocks: {len(self.chain)}\n"
        viz += f"Chain Valid: {'✓ Yes' if self.is_chain_valid() else '✗ No'}\n"
        
        return viz

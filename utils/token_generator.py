"""
Green Token Generator Module
Generates verifiable green tokens with cryptographic hashing
"""

import hashlib
import json
import uuid
from datetime import datetime

class GreenTokenGenerator:
    """
    Generates Verified Green Tokens with immutable cryptographic proof
    """
    
    def __init__(self):
        self.version = "1.0"
    
    def generate_token(self, token_data):
        """
        Generate a Verified Green Token with cryptographic hash
        
        Args:
            token_data: Dictionary containing token information
                - sme_id: SME identifier
                - sme_name: Name of the business
                - business_type: Type of business
                - month: Period of the token
                - energy_kwh: Energy consumed
                - emissions_kg: CO2 emissions in kg
                - emissions_reduced_kg: CO2 reduced vs baseline in kg
                - baseline_kg: Baseline emissions in kg
                - timestamp: Timestamp
        
        Returns:
            dict: Complete token with verification hash (CANONICAL SCHEMA)
        """
        # Generate unique token ID
        token_id = self._generate_token_id(token_data)
        
        # Create token structure (CANONICAL SCHEMA - always kg internally)
        token = {
            'token_id': token_id,
            'version': self.version,
            'sme_id': token_data['sme_id'],
            'sme_name': token_data['sme_name'],
            'business_type': token_data['business_type'],
            'month': token_data['month'],
            
            # ALWAYS kg internally - convert to tonnes only in UI
            'energy_kwh': float(token_data['energy_kwh']),
            'emissions_kg': float(token_data['emissions_kg']),
            'baseline_kg': float(token_data['baseline_kg']),
            'emissions_reduced_kg': float(token_data['emissions_reduced_kg']),
            
            'reduction_percentage': self._calculate_reduction_pct(
                token_data['emissions_reduced_kg'], 
                token_data['baseline_kg']
            ),
            'timestamp': token_data.get('timestamp', datetime.now().isoformat()),
            'status': 'verified'
        }
        
        # Generate immutable hash
        token['hash'] = self._generate_hash(token)
        
        # Generate blockchain-style signature
        token['signature'] = self._generate_signature(token)
        
        return token
    
    def _generate_token_id(self, token_data):
        """
        Generate unique token ID
        
        Args:
            token_data: Token data dictionary
        
        Returns:
            str: Unique token ID
        """
        # Create a unique identifier combining SME ID, month, and UUID
        base = f"{token_data['sme_id']}-{token_data['month']}"
        unique_suffix = str(uuid.uuid4())[:8]
        
        return f"GT-{base}-{unique_suffix}".upper()
    
    def _generate_hash(self, token):
        """
        Generate SHA-256 hash of token data (immutable proof)
        
        Args:
            token: Token dictionary (without hash)
        
        Returns:
            str: SHA-256 hash
        """
        # Create a copy without hash and signature fields
        token_copy = {k: v for k, v in token.items() if k not in ['hash', 'signature']}
        
        # Convert to JSON string (sorted keys for consistency)
        token_string = json.dumps(token_copy, sort_keys=True)
        
        # Generate SHA-256 hash
        hash_object = hashlib.sha256(token_string.encode())
        return hash_object.hexdigest()
    
    def _generate_signature(self, token):
        """
        Generate a blockchain-style signature
        
        Args:
            token: Token dictionary with hash
        
        Returns:
            str: Signature string
        """
        # Combine critical fields for signature
        signature_data = f"{token['token_id']}{token['timestamp']}{token['hash']}"
        
        # Create signature hash
        sig_object = hashlib.sha256(signature_data.encode())
        return sig_object.hexdigest()
    
    def _calculate_reduction_pct(self, reduction, baseline):
        """
        Calculate reduction percentage
        
        Args:
            reduction: Amount reduced
            baseline: Baseline value
        
        Returns:
            float: Reduction percentage
        """
        if baseline == 0:
            return 0.0
        
        return round((reduction / baseline) * 100, 2)
    
    def verify_token(self, token):
        """
        Verify token integrity by recalculating hash
        
        Args:
            token: Token dictionary to verify
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        if 'hash' not in token:
            return False
        
        # Store original hash
        original_hash = token['hash']
        
        # Recalculate hash
        recalculated_hash = self._generate_hash(token)
        
        # Compare hashes
        return original_hash == recalculated_hash
    
    def get_token_summary(self, token):
        """
        Get human-readable summary of token
        
        Args:
            token: Token dictionary (CANONICAL SCHEMA)
        
        Returns:
            str: Formatted summary
        """
        # Convert kg to tonnes for display
        emissions_tonnes = token['emissions_kg'] / 1000
        reduced_tonnes = token['emissions_reduced_kg'] / 1000
        
        summary = f"""
        ╔══════════════════════════════════════════════════════════════╗
        ║             VERIFIED GREEN TOKEN                              ║
        ╠══════════════════════════════════════════════════════════════╣
        ║ Token ID: {token['token_id']:<49} ║
        ║ SME: {token['sme_name']:<54} ║
        ║ Business Type: {token['business_type']:<44} ║
        ║ Period: {token['month']:<51} ║
        ╠══════════════════════════════════════════════════════════════╣
        ║ Energy Consumed: {token['energy_kwh']:.2f} kWh{' ' * (40 - len(f"{token['energy_kwh']:.2f}"))} ║
        ║ CO₂ Emissions: {token['emissions_kg']:.2f} kg (≈ {emissions_tonnes:.3f} tonnes){' ' * (20 - len(f"{emissions_tonnes:.3f}"))} ║
        ║ CO₂ Reduced: {token['emissions_reduced_kg']:.2f} kg (≈ {reduced_tonnes:.3f} tonnes){' ' * (22 - len(f"{reduced_tonnes:.3f}"))} ║
        ║ Reduction: {token['reduction_percentage']:.1f}%{' ' * (48 - len(f"{token['reduction_percentage']:.1f}"))} ║
        ╠══════════════════════════════════════════════════════════════╣
        ║ Status: VERIFIED ✓{' ' * 45} ║
        ║ Timestamp: {token['timestamp'][:19]:<45} ║
        ║ Hash: {token['hash'][:32]}...{' ' * (22)} ║
        ╚══════════════════════════════════════════════════════════════╝
        """
        return summary
    
    def export_token_json(self, token):
        """
        Export token as JSON string
        
        Args:
            token: Token dictionary
        
        Returns:
            str: JSON string
        """
        return json.dumps(token, indent=2, sort_keys=True)
    
    def create_verification_url(self, token, base_url="https://eco-chain-verify.example.com"):
        """
        Create a shareable verification URL
        
        Args:
            token: Token dictionary
            base_url: Base URL for verification service
        
        Returns:
            str: Verification URL
        """
        verification_params = f"token={token['token_id']}&hash={token['hash'][:16]}"
        return f"{base_url}/verify?{verification_params}"
    
    def batch_generate_tokens(self, token_data_list):
        """
        Generate multiple tokens at once
        
        Args:
            token_data_list: List of token data dictionaries
        
        Returns:
            list: List of generated tokens
        """
        tokens = []
        
        for token_data in token_data_list:
            token = self.generate_token(token_data)
            tokens.append(token)
        
        return tokens
    
    def get_token_metadata(self, token):
        """
        Extract metadata from token
        
        Args:
            token: Token dictionary
        
        Returns:
            dict: Metadata
        """
        return {
            'token_id': token['token_id'],
            'sme_id': token['sme_id'],
            'month': token['month'],
            'timestamp': token['timestamp'],
            'hash': token['hash'],
            'status': token['status'],
            'version': token['version']
        }

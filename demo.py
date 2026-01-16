#!/usr/bin/env python3
"""
Eco-Chain Demo Script
This script demonstrates all major features of the Eco-Chain platform
"""

import pandas as pd
import hashlib
from datetime import datetime

def demo_emission_calculation():
    """Demonstrate emission calculation logic"""
    print("=" * 70)
    print("DEMO 1: EMISSION CALCULATION")
    print("=" * 70)
    
    # Sample data
    energy_kwh = 10000
    region = "India"
    emission_factor = 0.82  # kg CO2 per kWh for India
    
    print(f"\nInput:")
    print(f"  Energy Consumption: {energy_kwh:,} kWh")
    print(f"  Region: {region}")
    print(f"  Emission Factor: {emission_factor} kg CO₂/kWh")
    
    # Calculate
    emissions_kg = energy_kwh * emission_factor
    emissions_tonnes = emissions_kg / 1000
    
    print(f"\nCalculation:")
    print(f"  {energy_kwh:,} kWh × {emission_factor} kg CO₂/kWh = {emissions_kg:,.0f} kg CO₂")
    print(f"  {emissions_kg:,.0f} kg ÷ 1000 = {emissions_tonnes:.2f} tonnes CO₂")
    
    print(f"\n✅ Result: {emissions_tonnes:.2f} tonnes CO₂ emitted")
    print()

def demo_baseline_comparison():
    """Demonstrate baseline comparison"""
    print("=" * 70)
    print("DEMO 2: BASELINE COMPARISON")
    print("=" * 70)
    
    # Sample data
    industry = "Food Processing"
    your_energy = 9000
    baseline_energy = 12000
    emission_factor = 0.82
    
    print(f"\nScenario:")
    print(f"  Industry: {industry}")
    print(f"  Industry Baseline: {baseline_energy:,} kWh/month")
    print(f"  Your Energy Use: {your_energy:,} kWh/month")
    
    # Calculate
    your_emissions = (your_energy * emission_factor) / 1000
    baseline_emissions = (baseline_energy * emission_factor) / 1000
    reduction = baseline_emissions - your_emissions
    efficiency_ratio = your_energy / baseline_energy
    
    print(f"\nYour Performance:")
    print(f"  Your Emissions: {your_emissions:.2f} tonnes CO₂")
    print(f"  Baseline Emissions: {baseline_emissions:.2f} tonnes CO₂")
    print(f"  Reduction Achieved: {reduction:.2f} tonnes CO₂")
    print(f"  Efficiency Ratio: {efficiency_ratio:.2f}")
    
    if efficiency_ratio < 0.7:
        rating = "🏆 EXCELLENT"
    elif efficiency_ratio < 0.9:
        rating = "⭐ GOOD"
    elif efficiency_ratio < 1.1:
        rating = "👍 AVERAGE"
    else:
        rating = "⚠️ NEEDS IMPROVEMENT"
    
    print(f"\n✅ Performance Rating: {rating}")
    print(f"✅ You're {((1 - efficiency_ratio) * 100):.1f}% better than industry average!")
    print()

def demo_token_generation():
    """Demonstrate green token generation and hashing"""
    print("=" * 70)
    print("DEMO 3: GREEN TOKEN GENERATION")
    print("=" * 70)
    
    # Sample data
    sme_id = "MSME123456"
    sme_name = "Ravi Manufacturing Pvt Ltd"
    emissions_reduced = 2.46
    timestamp = datetime.now().isoformat()
    
    print(f"\nToken Input:")
    print(f"  SME ID: {sme_id}")
    print(f"  SME Name: {sme_name}")
    print(f"  Emissions Reduced: {emissions_reduced:.2f} tonnes")
    print(f"  Timestamp: {timestamp}")
    
    # Generate hash
    data_string = f"{sme_id}|{emissions_reduced}|{timestamp}"
    hash_object = hashlib.sha256(data_string.encode())
    verification_hash = hash_object.hexdigest()
    
    print(f"\nCryptographic Process:")
    print(f"  Combined String: '{data_string}'")
    print(f"  Hash Algorithm: SHA-256")
    print(f"  Verification Hash: {verification_hash}")
    
    token = {
        "token_id": "ECO-000001",
        "sme_id": sme_id,
        "sme_name": sme_name,
        "emissions_reduced_tonnes": emissions_reduced,
        "timestamp": timestamp,
        "verification_hash": verification_hash,
        "status": "VERIFIED"
    }
    
    print(f"\n✅ Green Token Issued:")
    for key, value in token.items():
        if key == "verification_hash":
            print(f"  {key}: {value[:32]}...")
        else:
            print(f"  {key}: {value}")
    print()

def demo_merkle_tree():
    """Demonstrate Merkle tree for registry integrity"""
    print("=" * 70)
    print("DEMO 4: MERKLE TREE VERIFICATION")
    print("=" * 70)
    
    # Sample token hashes
    token_hashes = [
        hashlib.sha256(b"token1").hexdigest(),
        hashlib.sha256(b"token2").hexdigest(),
        hashlib.sha256(b"token3").hexdigest(),
        hashlib.sha256(b"token4").hexdigest(),
    ]
    
    print(f"\nToken Registry (4 tokens):")
    for i, hash_val in enumerate(token_hashes, 1):
        print(f"  Token {i}: {hash_val[:32]}...")
    
    # Build Merkle tree
    def create_merkle_root(hashes):
        if len(hashes) == 1:
            return hashes[0]
        
        new_level = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                combined = hashes[i] + hashes[i + 1]
            else:
                combined = hashes[i] + hashes[i]
            new_level.append(hashlib.sha256(combined.encode()).hexdigest())
        
        return create_merkle_root(new_level)
    
    merkle_root = create_merkle_root(token_hashes)
    
    print(f"\nMerkle Tree Construction:")
    print(f"  Level 1 (Tokens): 4 hashes")
    print(f"  Level 2 (Pairs): 2 combined hashes")
    print(f"  Level 3 (Root): 1 final hash")
    
    print(f"\n✅ Merkle Root: {merkle_root[:32]}...")
    print("✅ Entire registry integrity proven with single hash!")
    print("⚠️  Any tampering would change the Merkle root")
    print()

def demo_ai_suggestions():
    """Demonstrate data-driven sustainability recommendations"""
    print("=" * 70)
    print("DEMO 5: DATA-DRIVEN RECOMMENDATIONS")
    print("=" * 70)
    
    # Sample data
    industry = "Textile Manufacturing"
    energy_consumed = 16500
    baseline_energy = 15000
    efficiency_ratio = energy_consumed / baseline_energy
    
    print(f"\nBusiness Profile:")
    print(f"  Industry: {industry}")
    print(f"  Monthly Energy: {energy_consumed:,} kWh")
    print(f"  Industry Baseline: {baseline_energy:,} kWh")
    print(f"  Efficiency Ratio: {efficiency_ratio:.2f}")
    
    print(f"\n📊 Analysis:")
    print(f"  Status: Energy use is {((efficiency_ratio - 1) * 100):.1f}% above baseline")
    print(f"  Priority: Implement energy efficiency measures")
    
    print(f"\n💡 Data-Driven Recommendations:")
    
    print(f"\n1. 🔴 HIGH PRIORITY: Energy Audit")
    print(f"   Description: Professional audit to identify inefficiencies")
    print(f"   Potential Savings: {(energy_consumed * 0.10):.0f} kWh/month")
    print(f"   Why: You're {((efficiency_ratio - 1) * 100):.1f}% above industry standard")
    
    print(f"\n2. 🟡 MEDIUM PRIORITY: Solar Panel Installation")
    print(f"   Description: Rooftop solar to offset 20-30% of consumption")
    print(f"   Potential Savings: {(energy_consumed * 0.25):.0f} kWh/month")
    print(f"   ROI: Typical payback 3-5 years")
    
    print(f"\n3. 🟡 MEDIUM PRIORITY: Equipment Upgrade")
    print(f"   Description: Replace motors >10 years with 5-star rated")
    print(f"   Potential Savings: {(energy_consumed * 0.20):.0f} kWh/month")
    print(f"   Impact: 15-25% energy savings possible")
    
    print(f"\n4. 🟡 MEDIUM PRIORITY: Load Shifting")
    print(f"   Description: Shift 30-40% operations to off-peak hours")
    print(f"   Potential Savings: {(energy_consumed * 0.15):.0f} kWh equivalent CO₂")
    print(f"   Benefit: Lower carbon intensity from grid")
    
    print(f"\n✅ Total Potential Savings: {(energy_consumed * 0.50):.0f} kWh/month")
    print(f"✅ Could improve efficiency ratio to: {((energy_consumed * 0.5) / baseline_energy):.2f}")
    print()

def demo_environmental_impact():
    """Demonstrate environmental impact equivalents"""
    print("=" * 70)
    print("DEMO 6: ENVIRONMENTAL IMPACT")
    print("=" * 70)
    
    # Sample data
    co2_reduced = 5.5  # tonnes
    
    print(f"\nCO₂ Reduction Achieved: {co2_reduced:.2f} tonnes")
    
    # Calculate equivalents
    trees = int(co2_reduced * 40)  # 1 tonne = ~40 trees/year
    cars = int(co2_reduced * 0.22)  # 1 tonne = ~0.22 cars/year
    homes = int(co2_reduced * 0.11)  # 1 tonne = ~0.11 homes/month
    
    print(f"\n🌍 Real-World Equivalents:")
    print(f"\n  🌳 Trees Planted: {trees:,} trees")
    print(f"     (Grown for 1 year to absorb this CO₂)")
    
    print(f"\n  🚗 Cars Off Road: {cars} passenger vehicles")
    print(f"     (Removed for 1 year)")
    
    print(f"\n  🏠 Homes Powered: {homes} homes")
    print(f"     (Powered sustainably for 1 month)")
    
    print(f"\n  ⚡ Clean Energy: {(co2_reduced * 1000 / 0.82):.0f} kWh")
    print(f"     (Equivalent renewable energy)")
    
    print(f"\n✅ Your sustainability makes a real difference!")
    print()

def demo_verification_process():
    """Demonstrate public verification process"""
    print("=" * 70)
    print("DEMO 7: PUBLIC VERIFICATION")
    print("=" * 70)
    
    # Sample token
    token = {
        "token_id": "ECO-000042",
        "sme_name": "Green Manufacturing Co.",
        "emissions_reduced_tonnes": 3.25,
        "timestamp": "2025-01-14T10:30:00",
        "verification_hash": hashlib.sha256(b"sample_token").hexdigest(),
        "status": "VERIFIED"
    }
    
    print(f"\nScenario: Buyer wants to verify sustainability claim")
    print(f"\nStep 1: SME provides verification hash")
    print(f"  Hash: {token['verification_hash'][:32]}...")
    
    print(f"\nStep 2: Buyer enters hash in Eco-Chain verification portal")
    
    print(f"\nStep 3: System validates token")
    print(f"  ✅ Hash found in registry")
    print(f"  ✅ Token not tampered")
    print(f"  ✅ Timestamp verified")
    print(f"  ✅ Merkle tree confirmed")
    
    print(f"\nStep 4: Verified details displayed")
    print(f"  Token ID: {token['token_id']}")
    print(f"  Business: {token['sme_name']}")
    print(f"  CO₂ Reduced: {token['emissions_reduced_tonnes']:.2f} tonnes")
    print(f"  Date: {token['timestamp'][:10]}")
    print(f"  Status: {token['status']}")
    
    print(f"\n✅ Verification Complete!")
    print(f"✅ Buyer trusts SME's sustainability claim")
    print(f"✅ SME wins contract based on verified proof")
    print()

def demo_complete_workflow():
    """Demonstrate complete workflow from data to certificate"""
    print("=" * 70)
    print("DEMO 8: COMPLETE WORKFLOW")
    print("=" * 70)
    
    print(f"\n📋 SCENARIO: Ravi's Manufacturing Unit")
    print(f"=" * 70)
    
    print(f"\nStep 1: Collect Data")
    print(f"  ✅ November 2024: 8,500 kWh")
    print(f"  ✅ December 2024: 7,800 kWh")
    print(f"  ✅ January 2025: 7,200 kWh")
    
    print(f"\nStep 2: Calculate Emissions")
    total_energy = 8500 + 7800 + 7200
    total_emissions = (total_energy * 0.82) / 1000
    baseline_emissions = (10000 * 3 * 0.82) / 1000
    reduction = baseline_emissions - total_emissions
    
    print(f"  Total Energy: {total_energy:,} kWh")
    print(f"  Emissions: {total_emissions:.2f} tonnes CO₂")
    print(f"  Baseline: {baseline_emissions:.2f} tonnes CO₂")
    print(f"  ✅ Reduction: {reduction:.2f} tonnes CO₂")
    
    print(f"\nStep 3: Issue Green Token")
    token_id = "ECO-000001"
    verification_hash = hashlib.sha256(f"MSME123456|{reduction}|{datetime.now().isoformat()}".encode()).hexdigest()
    print(f"  ✅ Token ID: {token_id}")
    print(f"  ✅ Hash: {verification_hash[:32]}...")
    print(f"  ✅ Status: VERIFIED")
    
    print(f"\nStep 4: Generate Certificate")
    print(f"  ✅ PDF created with all details")
    print(f"  ✅ Includes verification QR code")
    print(f"  ✅ Shows monthly breakdown")
    print(f"  ✅ Environmental impact included")
    
    print(f"\nStep 5: Share with Stakeholders")
    print(f"  ✅ Email certificate to buyer")
    print(f"  ✅ Attach to bank loan application")
    print(f"  ✅ Submit for government incentive")
    print(f"  ✅ Post on company website")
    
    print(f"\nStep 6: Verification by Stakeholder")
    print(f"  ✅ Buyer checks hash on public portal")
    print(f"  ✅ Confirms authenticity")
    print(f"  ✅ Trusts sustainability claim")
    
    print(f"\nStep 7: Business Impact")
    print(f"  🎉 Won new contract worth ₹50 lakhs")
    print(f"  🎉 Bank approved green loan at lower rate")
    print(f"  🎉 Qualified for government subsidy")
    print(f"  🎉 Brand reputation improved")
    
    print(f"\n✅ SUCCESS: Ravi's sustainability efforts recognized and rewarded!")
    print()

def run_all_demos():
    """Run streamlined 90-second demonstration"""
    print("\n" + "=" * 70)
    print("ECO-CHAIN - 90 SECOND DEMONSTRATION")
    print("=" * 70)
    print("\n🎯 DEMO FLOW (90 seconds):")
    print("  1. Scenario (Ravi)")
    print("  2. Calculate emissions")
    print("  3. Issue token")
    print("  4. Download certificate")
    print("  5. Verify publicly")
    print("\n⏱️  Technical details available on request.\n")
    
    input("Press Enter to start the 90-second demo...")
    demo_complete_workflow()
    
    print("\n" + "=" * 70)
    print("90-SECOND DEMO COMPLETE!")
    print("=" * 70)
    print("\n📋 What judges saw:")
    print("  ✅ Real problem (Ravi can't prove sustainability)")
    print("  ✅ Simple upload → Verified proof")
    print("  ✅ Professional certificate")
    print("  ✅ Public verification")
    print("  ✅ Clear business value")
    
    print("\n" + "=" * 70)
    print("ADDITIONAL TECHNICAL DEMOS (Optional)")
    print("=" * 70)
    print("\n💡 Available if judges ask:")
    print("  1. Emission calculation methodology")
    print("  2. Baseline comparison logic")
    print("  3. Token generation & cryptographic hashing")
    print("  4. Merkle tree verification")
    print("  5. Recommendation engine")
    print("  6. Environmental impact equivalents")
    print("  7. Public verification deep-dive")
    
    show_more = input("\n🔍 Show technical demos? (y/N): ").lower()
    
    if show_more == 'y':
        print("\n" + "=" * 70)
        print("TECHNICAL DEEP-DIVE")
        print("=" * 70)
        
        input("\nPress Enter for Demo 1 (Emission Calculation)...")
        demo_emission_calculation()
        
        input("Press Enter for Demo 2 (Baseline Comparison)...")
        demo_baseline_comparison()
        
        input("Press Enter for Demo 3 (Token Generation)...")
        demo_token_generation()
        
        input("Press Enter for Demo 4 (Merkle Tree)...")
        demo_merkle_tree()
        
        input("Press Enter for Demo 5 (Recommendations)...")
        demo_ai_suggestions()
        
        input("Press Enter for Demo 6 (Environmental Impact)...")
        demo_environmental_impact()
        
        input("Press Enter for Demo 7 (Verification)...")
        demo_verification_process()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE!")
    print("=" * 70)
    print("\n🌱 Eco-Chain: Making sustainability verification accessible to SMEs")
    print("⏱️  Remember: Lead with the 90-second demo. Details only if asked.")
    print()

if __name__ == "__main__":
    run_all_demos()

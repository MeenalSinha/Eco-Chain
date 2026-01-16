# 🌱 Eco-Chain - Verifiable Sustainability Proof for Small Businesses

**Eco-Chain transforms electricity consumption data into cryptographically verified sustainability certificates that SMEs can share with buyers, banks, and regulators—without expensive audits.**

Built by: [Your Name/Team Name] | Competition: Ideas for India Innovation Challenge 2025

---

## ⚡ 30-Second Overview

- **What:** Generates verifiable sustainability proof for SMEs from energy data  
- **Who:** Manufacturing & textile SMEs that lose contracts due to lack of proof  
- **Why:** Audits are expensive (₹50K-500K); carbon credits built for large enterprises  
- **How:** Emissions calculation + cryptographic verification (SHA-256) + shareable certificates  
- **Status:** Fully functional MVP with 90-second demo ready

---

## Quick Start

**Run locally:**
```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at `http://localhost:8501`

**Tech Stack:** Python + Streamlit + Plotly + ReportLab | SHA-256 hashing + Merkle trees

---

## The Problem

SMEs invest in green practices but **cannot prove it**:
- Carbon credits are for large corporations
- Audits cost ₹50,000-500,000 and take months
- Buyers, banks, governments demand proof SMEs don't have
- Result: Honest businesses lose while greenwashing survives

**Built for manufacturing and textile SMEs like Ravi who lose contracts because they can't prove sustainability.**

---

## The Solution

Three steps:
1. **Calculate** - CO₂ emissions from energy data
2. **Lock** - Cryptographic verification (SHA-256)
3. **Issue** - Shareable certificate

No auditors. No expensive compliance. No greenwashing.

> **Important**: Eco-Chain issues verification tokens for sustainability proof, NOT tradeable carbon credits.

> **Data Sources**: Emission factors based on publicly available IEA/EPA averages (demo implementation).

---

## Core Features

**Carbon Proof Generator** - Upload bills/manual entry, calculate vs industry baseline, 5 industries × 5 regions

**Verified Green Tokens** - SHA-256 secured with Merkle tree simulation, unique ID + hash + timestamp

**Downloadable Certificates** - Professional PDFs with QR codes, displays kg and tonnes for clarity

**Interactive Dashboard** - Emissions trends, performance badges, token registry, impact equivalents

**Data-Driven Recommendations** - Rule-based suggestions with costs, payback periods, priority ranking

**Public Verification** - Hash validation, transparent registry, blockchain-style proof of inclusion

---

## How It Works

**Emission Calculation:**
```
Emissions (tonnes CO₂) = Energy (kWh) × Regional Factor (kg CO₂/kWh) ÷ 1000
```

Factors: India 0.82, USA 0.42, EU 0.28, China 0.58

**Baseline Comparison:**  
Textile: 15,000 kWh/month | Food: 12,000 | Manufacturing: 10,000 | Retail: 5,000 | Tech: 3,000

**Token Generation:**  
```
Hash = SHA256(SME_ID | Emissions_Reduced | Timestamp)
```

**Merkle Tree:** All tokens combined into one root for tamper evidence

---

## Tech Stack

**Frontend:** Streamlit-based dashboard with Plotly interactive visualizations  
**Backend:** Python 3.9+, modular architecture

**Core Modules:**
- `carbon_calculator.py` - IEA/EPA emissions calculations
- `token_generator.py` - Cryptographic token generation  
- `blockchain_simulator.py` - Ledger simulation with Merkle trees
- `certificate_generator.py` - PDF certificate generation
- `ai_suggestions.py` - Rule-based recommendations

**Security:** SHA-256 hashing, Merkle trees, timestamp verification

**Dependencies:** streamlit, pandas, plotly, reportlab, qrcode, pillow

---

## Usage

1. Navigate to "Calculate Emissions"
2. Enter business info (ID, name, industry, region)
3. Upload CSV or enter data manually
4. Click "Calculate" → Get token → Download certificate
5. Share with buyers/banks/regulators

**CSV Format:**
```csv
Month,Energy_kWh
January 2025,8500
February 2025,7800
```

---

## Demo Scenario

**Ravi** (manufacturing owner):
1. Uploads 3 months: 23,500 kWh total
2. System calculates: 19.27 tonnes CO₂
3. vs Baseline: 24.6 tonnes
4. **Reduced: 5.33 tonnes**
5. Token issued: GT-MSME123456-...
6. Certificate → Buyer → Verified → Contract won

*(Demo values for illustration)*

---

## What's Working

✅ All core features functional  
✅ Modular, production-ready code  
✅ Clean, modern Streamlit UI  
✅ Comprehensive docs  
✅ 90-second demo ready

---

## Known Limitations

**Technical:**
- Session state (no database yet)
- Cryptographic ledger simulation (not actual blockchain)
- Manual data entry required

**Scope:**
- Demo implementation of factors
- Electricity only (no gas/diesel)
- Rule-based recommendations (not ML)

**Mitigation:**
- Database integration planned
- Blockchain deployment possible (Polygon/Sepolia)
- IoT sensors roadmap

---

## Roadmap

### General Timeline
**Next 3 months:** Database, authentication, multi-user  
**6 months:** Blockchain deployment, IoT, mobile app  
**12 months:** API, government integration, bank partnerships

### If Selected for Finals (48-hour sprint)
- **Buyer-side verification dashboard** - Portal for buyers to verify multiple SME certificates
- **Real SME pilot** - Test with 5-10 actual manufacturing units using their electricity bills
- **Export-ready ESG reports** - Generate standardized reports for bank/government submission
- **Multi-language support** - Hindi + regional language interface for wider SME access

---

## Additional Documentation

- **QUICKSTART.md** - 3-minute setup guide
- **USER_GUIDE.md** - Detailed walkthrough with screenshots
- **SUBMISSION_DESCRIPTION.md** - Competition pitch (90-second demo)
- **sample_data.csv** - Test data included

---

## Acknowledgments

Emission factors from IEA/EPA. Not affiliated with carbon trading platforms.

Built to make sustainability verification accessible to small businesses.

---

## License

MIT License - Free to use, modify, distribute

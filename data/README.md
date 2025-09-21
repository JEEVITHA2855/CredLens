# CredLens Dataset

This directory contains the sample fact-checking dataset for CredLens.

## Files

- `build_dataset.py` - Main script to build the dataset
- `raw/` - Raw dataset files and demo scenarios  
- `processed/` - Processed files (FAISS index, embeddings)

## Building the Dataset

Run the dataset builder from the project root:

```bash
cd e:\CredLens
python data\build_dataset.py
```

This will:
1. Create a SQLite database with 50+ fact-checks
2. Generate demo scenarios for testing
3. Create a dataset summary

## Dataset Contents

The dataset includes fact-checks across multiple categories:
- Vaccines & Health (COVID-19, general health claims)
- Climate Change (temperature, causes, impacts)
- Technology (5G, internet, devices)
- Politics & Elections (voting, governance)
- Economics (policy impacts, markets)
- History (historical events, conspiracy theories)
- Food & Agriculture (GMOs, organic food, nutrition)
- Environment & Energy (renewable energy, pollution)
- Science & Space (evolution, flat earth, moon landing)
- Social Media & Technology (platform bias, digital privacy)

## Demo Scenarios

Four demo scenarios are included to test different verdict types:
1. **True Claim** - Should be verified as accurate
2. **False Claim** - Contains misinformation with sensational language
3. **Mixed Evidence** - Has both supporting and contradicting evidence
4. **Unverified** - Novel claim with no existing evidence

## Notes

- All fact-checks include source attribution
- Claims span different complexity levels for testing
- Dataset includes both clear-cut and nuanced cases
- Sources include reputable organizations (CDC, WHO, NASA, etc.)
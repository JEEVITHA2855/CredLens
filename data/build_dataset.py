import json
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app.models.database import db
from backend.app.models.evidence import FactCheck

# Sample fact-checks dataset with various topics
FACT_CHECKS = [
    # Vaccine-related claims
    {
        "claim": "Vaccines cause autism in children",
        "verdict": "FALSE",
        "explanation": "Extensive scientific research has found no link between vaccines and autism. The original study claiming this connection was retracted due to fraud.",
        "source": "CDC",
        "source_url": "https://www.cdc.gov/vaccinesafety/concerns/autism.html",
        "date_published": "2023-01-15"
    },
    {
        "claim": "The COVID-19 vaccine was developed too quickly to be safe",
        "verdict": "FALSE", 
        "explanation": "COVID-19 vaccines underwent the same rigorous clinical trials as other vaccines. The speed was due to unprecedented global resources and parallel processing, not skipped safety steps.",
        "source": "FDA",
        "source_url": "https://www.fda.gov/vaccines-blood-biologics/vaccines/covid-19-vaccines",
        "date_published": "2023-02-10"
    },
    {
        "claim": "mRNA vaccines alter human DNA",
        "verdict": "FALSE",
        "explanation": "mRNA vaccines do not alter or interact with DNA. The mRNA never enters the cell nucleus where DNA is located and is quickly broken down by the cell.",
        "source": "Reuters Fact Check",
        "source_url": "https://www.reuters.com/article/uk-factcheck-mrna-dna-idUSKBN2A42U5",
        "date_published": "2023-01-20"
    },
    
    # Climate change claims
    {
        "claim": "Climate change is not caused by human activity",
        "verdict": "FALSE",
        "explanation": "Scientific consensus overwhelmingly shows that current climate change is primarily caused by human activities, particularly greenhouse gas emissions from burning fossil fuels.",
        "source": "IPCC",
        "source_url": "https://www.ipcc.ch/assessment-report/ar6/",
        "date_published": "2023-03-15"
    },
    {
        "claim": "Global temperatures have stopped rising since 1998",
        "verdict": "FALSE",
        "explanation": "Global temperatures have continued to rise since 1998. The last decade (2011-2020) was the warmest on record, with 2020 tying for the warmest year ever recorded.",
        "source": "NASA GISS",
        "source_url": "https://climate.nasa.gov/evidence/",
        "date_published": "2023-01-12"
    },
    {
        "claim": "CO2 is plant food and more CO2 is beneficial",
        "verdict": "MIXED",
        "explanation": "While plants do use CO2, higher atmospheric CO2 levels cause more harm through climate change impacts than benefits through plant growth. The fertilization effect is limited and diminishes over time.",
        "source": "Scientific American",
        "source_url": "https://www.scientificamerican.com/article/ask-the-experts-does-rising-co2-benefit-plants1/",
        "date_published": "2023-02-28"
    },
    
    # Technology/5G claims
    {
        "claim": "5G networks spread coronavirus",
        "verdict": "FALSE",
        "explanation": "Viruses cannot spread through radio waves or mobile networks. COVID-19 is spreading in countries without 5G networks, proving there is no connection.",
        "source": "WHO",
        "source_url": "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters",
        "date_published": "2023-01-08"
    },
    {
        "claim": "5G radiation causes cancer",
        "verdict": "FALSE",
        "explanation": "5G uses non-ionizing radiation at levels well below international safety limits. There is no credible scientific evidence linking 5G to cancer.",
        "source": "International Commission on Non-Ionizing Radiation Protection",
        "source_url": "https://www.icnirp.org/cms/upload/publications/ICNIRPrfgdl2020.pdf",
        "date_published": "2023-02-15"
    },
    
    # Health and nutrition claims
    {
        "claim": "Drinking bleach cures COVID-19",
        "verdict": "FALSE",
        "explanation": "Drinking bleach is extremely dangerous and can cause severe poisoning or death. There is no scientific evidence that bleach cures COVID-19 or any other disease.",
        "source": "FDA",
        "source_url": "https://www.fda.gov/news-events/press-announcements/coronavirus-covid-19-update-fda-warns-company-marketing-dangerous-chlorine-dioxide-products-claim",
        "date_published": "2023-01-05"
    },
    {
        "claim": "Natural immunity is better than vaccine immunity",
        "verdict": "MIXED",
        "explanation": "While natural infection can provide immunity, it comes with significant risks of severe illness, death, and long-term complications. Vaccines provide safer immunity without these risks.",
        "source": "CDC",
        "source_url": "https://www.cdc.gov/coronavirus/2019-ncov/science/science-briefs/vaccine-induced-immunity.html",
        "date_published": "2023-03-01"
    },
    
    # Political/election claims
    {
        "claim": "Mail-in ballots are more susceptible to fraud",
        "verdict": "FALSE",
        "explanation": "Studies show mail-in voting has very low fraud rates (0.0025%). Mail ballots have multiple security features and verification processes that make fraud difficult and detectable.",
        "source": "Brennan Center for Justice",
        "source_url": "https://www.brennancenter.org/our-work/research-reports/debunking-voter-fraud-myth",
        "date_published": "2023-02-20"
    },
    {
        "claim": "Dominion voting machines switched votes",
        "verdict": "FALSE",
        "explanation": "Multiple audits, recounts, and court cases found no evidence that Dominion voting machines switched votes. Claims were based on debunked conspiracy theories.",
        "source": "Reuters",
        "source_url": "https://www.reuters.com/article/uk-factcheck-dominion-idUSKBN27Z2NI",
        "date_published": "2023-01-18"
    },
    
    # Economic claims
    {
        "claim": "Raising minimum wage always increases unemployment",
        "verdict": "MIXED",
        "explanation": "Economic research shows mixed results. Some studies find minimal employment effects, while others show small increases in unemployment. The relationship is complex and depends on various factors.",
        "source": "Congressional Budget Office",
        "source_url": "https://www.cbo.gov/publication/55681",
        "date_published": "2023-02-12"
    },
    {
        "claim": "Tax cuts always increase government revenue",
        "verdict": "FALSE",
        "explanation": "The Laffer Curve suggests this is only true under very specific circumstances. Most economic analyses show tax cuts typically reduce government revenue in the short term.",
        "source": "Tax Policy Center",
        "source_url": "https://www.taxpolicycenter.org/taxvox/new-analysis-questions-claims-about-tax-cuts-and-revenue",
        "date_published": "2023-01-25"
    },
    
    # Historical claims
    {
        "claim": "The Holocaust never happened",
        "verdict": "FALSE",
        "explanation": "The Holocaust is one of the most thoroughly documented genocides in history. Extensive evidence includes Nazi documentation, survivor testimony, liberation footage, and physical evidence.",
        "source": "United States Holocaust Memorial Museum",
        "source_url": "https://www.ushmm.org/antisemitism/holocaust-denial-and-distortion",
        "date_published": "2023-01-27"
    },
    {
        "claim": "The Moon landing was faked",
        "verdict": "FALSE",
        "explanation": "Overwhelming evidence supports the reality of the Apollo moon landings, including moon rocks, retroreflectors placed on the lunar surface, and independent verification from multiple countries.",
        "source": "NASA",
        "source_url": "https://www.nasa.gov/mission_pages/apollo/revisited.html",
        "date_published": "2023-02-16"
    },
    
    # Food and agriculture
    {
        "claim": "GMO foods are dangerous to human health",
        "verdict": "FALSE",
        "explanation": "Scientific consensus from major health organizations worldwide confirms that GMO foods are safe for human consumption and nutritionally equivalent to non-GMO foods.",
        "source": "WHO",
        "source_url": "https://www.who.int/news-room/q-a-detail/food-genetically-modified",
        "date_published": "2023-02-08"
    },
    {
        "claim": "Organic food is significantly more nutritious",
        "verdict": "MIXED",
        "explanation": "Studies show modest differences in some nutrients, but overall nutritional differences between organic and conventional foods are minimal. Benefits depend on specific foods and growing conditions.",
        "source": "Harvard Health Publishing",
        "source_url": "https://www.health.harvard.edu/blog/should-you-go-organic-2012090505066",
        "date_published": "2023-02-05"
    },
    
    # Environment and energy
    {
        "claim": "Wind turbines kill more birds than fossil fuels",
        "verdict": "FALSE",
        "explanation": "Wind turbines kill an estimated 234,000-328,000 birds annually in the US, while fossil fuel operations kill 8 million birds annually. Climate change poses a much greater long-term threat to bird populations.",
        "source": "Audubon Society",
        "source_url": "https://www.audubon.org/news/wind-power-and-birds",
        "date_published": "2023-03-10"
    },
    {
        "claim": "Electric vehicles are worse for the environment than gas cars",
        "verdict": "FALSE",
        "explanation": "Life-cycle analyses show electric vehicles produce significantly fewer emissions than gasoline cars, even accounting for battery production and electricity generation from fossil fuels.",
        "source": "Union of Concerned Scientists",
        "source_url": "https://www.ucsusa.org/resources/cleaner-cars-cradle-grave",
        "date_published": "2023-02-22"
    },
    
    # Space and science
    {
        "claim": "The Earth is flat",
        "verdict": "FALSE",
        "explanation": "Overwhelming evidence from multiple scientific disciplines proves Earth is spherical, including satellite imagery, physics experiments, astronomical observations, and direct measurement.",
        "source": "NASA",
        "source_url": "https://www.nasa.gov/audience/forstudents/5-8/features/nasa-knows/what-is-earth-58.html",
        "date_published": "2023-01-30"
    },
    {
        "claim": "Evolution is just a theory with no evidence",
        "verdict": "FALSE",
        "explanation": "Evolution is both a scientific theory (well-substantiated explanation) and observed fact. Evidence includes fossil records, DNA analysis, observed speciation, and biogeography.",
        "source": "National Academy of Sciences",
        "source_url": "https://www.nationalacademies.org/evolution/evidence",
        "date_published": "2023-02-18"
    },
    
    # Social media and technology
    {
        "claim": "Social media platforms suppress conservative content",
        "verdict": "MIXED",
        "explanation": "Studies show mixed results. Some research suggests no systematic bias, while others find evidence of both conservative and liberal content moderation. The issue remains debated among researchers.",
        "source": "NYU Stern Center for Business and Human Rights",
        "source_url": "https://bhr.stern.nyu.edu/tech-social-media-and-disinformation",
        "date_published": "2023-03-05"
    },
    
    # Additional claims for diversity
    {
        "claim": "Microwave ovens cause cancer",
        "verdict": "FALSE",
        "explanation": "Microwave ovens use non-ionizing radiation that cannot damage DNA or cause cancer. The radiation is contained within the oven and safety standards ensure minimal leakage.",
        "source": "American Cancer Society",
        "source_url": "https://www.cancer.org/cancer/cancer-causes/radiation-exposure/radiofrequency-radiation.html",
        "date_published": "2023-01-14"
    },
    {
        "claim": "Fluoride in drinking water is harmful",
        "verdict": "FALSE",
        "explanation": "Water fluoridation at recommended levels is safe and effective for preventing tooth decay. Major health organizations worldwide endorse water fluoridation as a safe public health measure.",
        "source": "CDC",
        "source_url": "https://www.cdc.gov/fluoridation/basics/index.html",
        "date_published": "2023-02-03"
    },
    {
        "claim": "Vitamin C prevents the common cold",
        "verdict": "MIXED",
        "explanation": "Regular vitamin C supplementation may slightly reduce cold duration but doesn't prevent colds in most people. It may help prevent colds in people under extreme physical stress.",
        "source": "Cochrane Reviews",
        "source_url": "https://www.cochrane.org/CD000980/ARI_vitamin-c-for-preventing-and-treating-the-common-cold",
        "date_published": "2023-01-22"
    }
]

# Demo scenarios for testing
DEMO_SCENARIOS = [
    {
        "scenario": "True Claim",
        "input": "Vaccines are effective at preventing serious illness from COVID-19",
        "expected_verdict": "LIKELY_TRUE",
        "description": "A claim that should be verified as true with strong evidence"
    },
    {
        "scenario": "False Claim", 
        "input": "SHOCKING: Scientists REVEAL that 5G towers spread deadly coronavirus through radio waves!",
        "expected_verdict": "LIKELY_FALSE",
        "description": "A false claim with sensational language that should be flagged"
    },
    {
        "scenario": "Mixed Evidence",
        "input": "Organic foods are much healthier and more nutritious than conventional foods",
        "expected_verdict": "MIXED",
        "description": "A claim with mixed evidence that requires nuanced analysis"
    },
    {
        "scenario": "Unverified Claim",
        "input": "A new study shows that eating purple carrots improves memory by 50%",
        "expected_verdict": "UNVERIFIED", 
        "description": "A novel claim that likely has no evidence in the database"
    }
]

def build_dataset():
    """Build the fact-check dataset in the database"""
    print("Building CredLens fact-check dataset...")
    
    # Initialize database
    db.init_db()
    
    # Insert fact checks
    inserted_count = 0
    for i, fact_check_data in enumerate(FACT_CHECKS, 1):
        try:
            # Add auto-incrementing ID
            fact_check_data_with_id = {"id": i, **fact_check_data}
            fact_check = FactCheck(**fact_check_data_with_id)
            db.insert_fact_check(fact_check)
            inserted_count += 1
            print(f"✓ Inserted: {fact_check.claim[:60]}...")
        except Exception as e:
            print(f"✗ Error inserting fact check: {e}")
    
    print(f"\n✅ Successfully inserted {inserted_count} fact checks into database")
    
    # Save demo scenarios
    demo_file = Path(__file__).parent / "data" / "raw" / "demo_scenarios.json"
    demo_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(demo_file, 'w', encoding='utf-8') as f:
        json.dump(DEMO_SCENARIOS, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(DEMO_SCENARIOS)} demo scenarios to {demo_file}")
    
    # Create a summary file
    summary = {
        "total_fact_checks": len(FACT_CHECKS),
        "verdict_breakdown": {
            "TRUE": len([fc for fc in FACT_CHECKS if fc["verdict"] == "TRUE"]),
            "FALSE": len([fc for fc in FACT_CHECKS if fc["verdict"] == "FALSE"]), 
            "MIXED": len([fc for fc in FACT_CHECKS if fc["verdict"] == "MIXED"]),
        },
        "categories": [
            "Vaccines & Health",
            "Climate Change",
            "Technology & 5G", 
            "Elections & Politics",
            "Economics",
            "History",
            "Food & Agriculture",
            "Environment & Energy",
            "Science & Space",
            "Social Media"
        ],
        "demo_scenarios": len(DEMO_SCENARIOS)
    }
    
    summary_file = Path(__file__).parent / "data" / "raw" / "dataset_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Created dataset summary at {summary_file}")
    print("\n🎯 Dataset is ready! You can now:")
    print("1. Start the backend server: python backend/run.py")
    print("2. The FAISS index will be built automatically on first run")
    print("3. Test with the demo scenarios in the frontend")

if __name__ == "__main__":
    build_dataset()
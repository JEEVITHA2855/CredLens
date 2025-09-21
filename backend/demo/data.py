# Example claims for training
TRAINING_DATA = [
    # Misinformation (label: 1)
    ("The Earth is flat and scientists are lying to us.", 1),
    ("5G networks are spreading COVID-19 through radio waves.", 1),
    ("Vaccines contain microchips for tracking people.", 1),
    ("The moon landing was faked in a Hollywood studio.", 1),
    ("Climate change is a hoax created by scientists.", 1),
    ("Drinking bleach can cure COVID-19.", 1),
    ("The government is controlling the weather with secret technology.", 1),
    ("Aliens built the pyramids.", 1),
    ("All world leaders are actually reptilian aliens.", 1),
    ("COVID-19 is no worse than the common cold.", 1),
    
    # Credible Information (label: 0)
    # Scientific Facts - Astronomy
    ("The Earth revolves around the Sun once every 365 days.", 0),
    ("The Earth rotates on its axis, causing day and night cycles.", 0),
    ("The Moon orbits around the Earth approximately every 27 days.", 0),
    ("The Sun is a star at the center of our solar system.", 0),
    ("Mercury is the closest planet to the Sun in our solar system.", 0),
    
    # Scientific Facts - General
    ("Regular exercise helps improve cardiovascular health according to medical studies.", 0),
    ("The human body needs oxygen to survive.", 0),
    ("Washing hands helps prevent the spread of germs and bacteria.", 0),
    ("Vaccines help prevent serious diseases by stimulating the immune system.", 0),
    ("Climate change is causing global temperatures to rise.", 0),
    
    # Health Facts
    ("Drinking water helps maintain proper hydration and bodily functions.", 0),
    ("A balanced diet includes fruits, vegetables, and whole grains.", 0),
    ("Regular sleep patterns contribute to better mental health.", 0),
    ("Regular exercise can help reduce stress levels.", 0)
]

# Evidence database for additional context
EVIDENCE_DATABASE = {
    "vaccines": {
        "facts": [
            "Vaccines undergo rigorous safety testing",
            "Vaccines have successfully eradicated or greatly reduced many diseases",
            "The benefits of vaccination far outweigh the risks"
        ],
        "sources": [
            "World Health Organization",
            "Centers for Disease Control and Prevention",
            "National Institutes of Health"
        ]
    },
    "climate_change": {
        "facts": [
            "Global temperatures have risen significantly since the industrial revolution",
            "Human activities are the primary driver of observed climate change",
            "Rising sea levels are threatening coastal communities"
        ],
        "sources": [
            "NASA",
            "NOAA",
            "Intergovernmental Panel on Climate Change"
        ]
    },
    "covid19": {
        "facts": [
            "COVID-19 is caused by the SARS-CoV-2 virus",
            "The virus can spread through respiratory droplets",
            "Vaccines have been proven effective at preventing severe illness"
        ],
        "sources": [
            "World Health Organization",
            "Centers for Disease Control and Prevention",
            "National Institutes of Health"
        ]
    },
    "astronomy": {
        "facts": [
            "The Earth's orbit around the Sun takes approximately 365.25 days",
            "This orbital period defines one year",
            "The Earth's axis is tilted 23.5 degrees, causing seasons",
            "The Earth's rotation on its axis takes 24 hours"
        ],
        "sources": [
            "NASA",
            "European Space Agency",
            "International Astronomical Union",
            "National Observatory"
        ]
    }
}

# Source credibility ratings
SOURCE_CREDIBILITY = {
    "scientific": {
        "peer_reviewed_journals": 0.95,
        "research_institutions": 0.90,
        "academic_publications": 0.85
    },
    "government": {
        "health_organizations": 0.90,
        "regulatory_agencies": 0.85,
        "local_government": 0.80
    },
    "news": {
        "established_newspapers": 0.80,
        "fact_checking_sites": 0.85,
        "news_agencies": 0.75
    },
    "social_media": {
        "verified_experts": 0.70,
        "general_users": 0.30,
        "anonymous_sources": 0.10
    }
}
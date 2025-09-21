class ScientificValidator:
    # Scientific facts and their keywords
    SCIENTIFIC_FACTS = {
        'earth_orbit': {
            'keywords': ['earth', 'sun', 'revolve', 'orbit', '365', 'days', 'year'],
            'fact': 'The Earth revolves around the Sun once every 365.25 days',
            'confidence': 100
        },
        'year_length': {
            'keywords': ['365', 'days', 'year'],
            'fact': 'There are approximately 365 days in a year',
            'confidence': 100
        },
        'gravity': {
            'keywords': ['gravity', 'gravitational', 'force', 'mass', 'attract'],
            'fact': 'Gravity is a fundamental force that attracts masses',
            'confidence': 100
        },
        'planets': {
            'keywords': ['planet', 'solar system', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune'],
            'fact': 'The solar system contains eight official planets',
            'confidence': 100
        },
        'time_day': {
            'keywords': ['24', 'hours', 'day'],
            'fact': 'There are 24 hours in a day',
            'confidence': 100
        },
        'time_hour': {
            'keywords': ['60', 'minutes', 'hour'],
            'fact': 'There are 60 minutes in an hour',
            'confidence': 100
        },
        'time_minute': {
            'keywords': ['60', 'seconds', 'minute'],
            'fact': 'There are 60 seconds in a minute',
            'confidence': 100
        },
        'water_boiling': {
            'keywords': ['water', 'boil', '100', 'celsius', 'degrees'],
            'fact': 'Water boils at 100 degrees Celsius at standard pressure',
            'confidence': 100
        },
        'water_freezing': {
            'keywords': ['water', 'freeze', '0', 'celsius', 'degrees'],
            'fact': 'Water freezes at 0 degrees Celsius at standard pressure',
            'confidence': 100
        }
    }
    
    @classmethod
    def validate_scientific_claim(cls, text):
        text_lower = text.lower()
        
        # Check against known scientific facts
        for fact_type, fact_data in cls.SCIENTIFIC_FACTS.items():
            if all(keyword in text_lower for keyword in fact_data['keywords']):
                return {
                    'is_scientific': True,
                    'fact_type': fact_type,
                    'reference': fact_data['fact'],
                    'confidence': fact_data['confidence'],
                    'sources': [
                        "Scientific textbooks",
                        "Academic research papers",
                        "NASA database",
                        "Educational resources"
                    ]
                }
        
        # General scientific terms check
        scientific_terms = {
            'physics': ['physics', 'force', 'energy', 'mass', 'velocity', 'acceleration'],
            'chemistry': ['chemistry', 'molecule', 'atom', 'element', 'reaction'],
            'biology': ['biology', 'cell', 'organism', 'gene', 'evolution'],
            'astronomy': ['astronomy', 'planet', 'star', 'galaxy', 'universe']
        }
        
        for field, terms in scientific_terms.items():
            if any(term in text_lower for term in terms):
                return {
                    'is_scientific': True,
                    'fact_type': field,
                    'confidence': 80,
                    'sources': [
                        "Scientific literature",
                        "Academic databases",
                        "Educational materials"
                    ]
                }
        
        return {
            'is_scientific': False,
            'confidence': 0,
            'sources': []
        }
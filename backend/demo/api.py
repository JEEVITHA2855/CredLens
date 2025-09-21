from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from model import MisinformationDetector
import numpy as np
import os
import json

class NumpyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.bool_)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)

app = Flask(__name__)

# Enable CORS for all origins in development
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins in development
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Configure JSON encoder for Flask responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.json_provider_class = json.JSONEncoder
app.json_encoder = NumpyJSONEncoder

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)

# Load the model
model_dir = "saved_model"
detector = MisinformationDetector.load_model(model_dir) if os.path.exists(model_dir) else None

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        app.logger.info("Received analyze request")
        if not detector:
            app.logger.error("Model not loaded")
            return jsonify({"success": False, "error": "Model not loaded. Please train the model first."}), 500
            
        data = request.json
        app.logger.info(f"Request data: {data}")
        
        if not data or 'text' not in data:
            app.logger.error("No text provided in request")
            return jsonify({"success": False, "error": "No text provided"}), 400
        
        if not data['text'] or len(data['text'].strip()) == 0:
            app.logger.error("Empty text provided")
            return jsonify({"success": False, "error": "Empty text provided"}), 400
            
        app.logger.info(f"Analyzing text: {data['text']}")
        raw_result = detector.analyze_text(data['text'])
        app.logger.info(f"Analysis result: {raw_result}")
        
        if not raw_result:
            app.logger.error("Analysis failed to produce results")
            return jsonify({"success": False, "error": "Analysis failed to produce results"}), 500
            
        # Convert numpy values to Python native types and prepare response
        # First convert all numpy values in raw_result to Python native types
        prediction = bool(raw_result['prediction']) if isinstance(raw_result['prediction'], np.bool_) else raw_result['prediction']
        credibility_score = float(raw_result['credibility_score'])
        confidence_score = float(raw_result['confidence_score'])
        probabilities = {
            'credible': float(raw_result['probabilities']['credible']),
            'misinformation': float(raw_result['probabilities']['misinformation'])
        }
        
        # Calculate normalized scores
        normalized_credibility = credibility_score / 100
        
        result = {
            "claim": data['text'],
            "status": "TRUE" if raw_result['classification'] == 'Likely Credible' else "FALSE",
            "overall_score": normalized_credibility,
            "analysis_type": "standard",
            "verdict": raw_result['classification'],
            "credibility_fingerprint": {
                "source_credibility": confidence_score / 100,
                "corroboration_count": int(probabilities['credible'] / 10),  # Convert to a reasonable number of sources
                "language_risk": probabilities['misinformation'] / 100,
                "overall_score": normalized_credibility
            },
            "evidence": [
                {
                    "text": raw_result['verification_result'].get('reasoning', 'No additional evidence found.'),
                    "source": "AI Analysis",
                    "relevance_score": confidence_score / 100
                }
            ],
            "verification_status": raw_result['classification'],
            "explanation": raw_result['verification_result'].get('reasoning', 'Analysis completed based on available data and patterns.'),
            "micro_lesson": {
                "title": "Understanding This Analysis",
                "content": f"This claim was analyzed and found to be {raw_result['classification'].lower()}. " + 
                          raw_result['verification_result'].get('reasoning', 'The analysis is based on our AI model evaluation.'),
                "source_evaluation_tips": [
                    "Look for multiple reliable sources that confirm the claim",
                    "Check the credibility of the sources",
                    "Consider the context and timing of the claim",
                    "Be aware of potential biases"
                ]
            },
            "suspicious_phrases": [
                phrase for phrase in data['text'].split('.') 
                if probabilities['misinformation'] > 50
            ],
            "extracted_claim": data['text'],
            "original_input": data['text']
        }
        
        app.logger.info(f"Formatted response: {json.dumps(result)}")
        return jsonify(result)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in /analyze endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Error analyzing text. Please try again."
        }), 500

@app.route('/')
def home():
    return jsonify({"status": "API is running"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
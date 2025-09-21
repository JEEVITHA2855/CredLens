import os
import openai

def test_api_key():
    try:
        # Get the API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "❌ API key not found in environment"
            
        print(f"API Key found: {api_key[:10]}...")
            
        # Set the API key
        openai.api_key = api_key
        
        # Try a simple completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API is working!'"}],
            max_tokens=10,
            temperature=0.7
        )
        
        return f"✅ API is working! Response: {response.choices[0].message.content}"
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    print("\nTesting OpenAI API connection...")
    result = test_api_key()
    print(result)
    print()
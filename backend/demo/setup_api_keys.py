"""
Quick setup script for CredLens API keys.
This script will guide you through the API key setup process.
"""
import os
import sys
import webbrowser
from pathlib import Path

def print_header():
    print("🚀 CredLens API Keys Setup Wizard")
    print("=" * 50)
    print("This wizard will help you get all the API keys needed for CredLens")
    print()

def open_api_signup_pages():
    """Open API signup pages in browser."""
    print("🌐 Opening API signup pages in your browser...")
    print("Please sign up and get your API keys from these services:")
    print()
    
    apis = [
        ("Google Fact Check API", "https://console.cloud.google.com/"),
        ("Bing Search API", "https://portal.azure.com/"),
        ("News API", "https://newsapi.org/register"),
        ("OpenAI API (Optional)", "https://platform.openai.com/signup")
    ]
    
    for name, url in apis:
        print(f"📝 {name}: {url}")
        try:
            webbrowser.open(url)
        except:
            print(f"   (Please manually visit: {url})")
    
    print()
    print("💡 Tip: Keep these browser tabs open while you get your API keys")
    print()

def create_env_file():
    """Create .env file from template."""
    template_path = Path(".env.template")
    env_path = Path(".env")
    
    if env_path.exists():
        response = input("⚠️ .env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Keeping existing .env file")
            return True
    
    if template_path.exists():
        # Copy template to .env
        with open(template_path, 'r') as template_file:
            content = template_file.read()
        
        with open(env_path, 'w') as env_file:
            env_file.write(content)
        
        print(f"✅ Created .env file from template")
        return True
    else:
        print("❌ .env.template file not found")
        return False

def interactive_key_entry():
    """Interactive API key entry."""
    print("🔑 Interactive API Key Entry")
    print("Enter your API keys (press Enter to skip optional keys):")
    print()
    
    keys = {}
    
    # Required keys
    required_keys = [
        ("GOOGLE_FACTCHECK_API_KEY", "Google Fact Check API Key", True),
        ("BING_SEARCH_API_KEY", "Bing Search API Key", True), 
        ("NEWS_API_KEY", "News API Key", True),
    ]
    
    # Optional keys  
    optional_keys = [
        ("OPENAI_API_KEY", "OpenAI API Key (optional)", False),
        ("GOOGLE_API_KEY", "Google API Key (optional)", False),
        ("GOOGLE_CSE_ID", "Google Custom Search Engine ID (optional)", False),
    ]
    
    all_keys = required_keys + optional_keys
    
    for key_name, display_name, required in all_keys:
        while True:
            key_value = input(f"🔐 {display_name}: ").strip()
            
            if not key_value and required:
                print("❌ This key is required. Please enter a valid key.")
                continue
            elif not key_value:
                print("⏭️ Skipping optional key")
                break
            else:
                keys[key_name] = key_value
                print("✅ Key saved")
                break
        print()
    
    return keys

def update_env_file(keys):
    """Update .env file with new keys."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found. Creating from template first...")
        if not create_env_file():
            return False
    
    # Read current content
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Update keys
    updated_content = content
    for key_name, key_value in keys.items():
        # Replace the template value
        old_pattern = f"{key_name}=your_.*_here"
        new_value = f"{key_name}={key_value}"
        
        import re
        if re.search(f"{key_name}=", content):
            updated_content = re.sub(f"{key_name}=.*", new_value, updated_content)
        else:
            # Add new key
            updated_content += f"\n{new_value}"
    
    # Write back
    with open(env_path, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated .env file with {len(keys)} API keys")
    return True

def test_setup():
    """Run connectivity test."""
    print("🧪 Testing your API setup...")
    print()
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_api_connectivity.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running connectivity test: {str(e)}")
        return False

def main():
    """Main setup wizard."""
    print_header()
    
    print("Choose your setup method:")
    print("1. 🌐 Open signup pages and enter keys interactively")
    print("2. 📝 Just create .env template file (fill manually)")
    print("3. 🧪 Test existing setup")
    print("4. ❌ Exit")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        # Full interactive setup
        open_api_signup_pages()
        
        input("\n⏸️ Press Enter after you've obtained your API keys...")
        
        keys = interactive_key_entry()
        
        if keys:
            if update_env_file(keys):
                print("🎉 Setup complete! Testing your configuration...")
                test_setup()
            else:
                print("❌ Failed to update .env file")
        else:
            print("❌ No API keys entered")
    
    elif choice == "2":
        # Create template only
        if create_env_file():
            print("✅ Template created! Please edit .env file manually with your API keys")
            print("💡 Run 'python setup_api_keys.py' again and choose option 3 to test")
        else:
            print("❌ Failed to create template")
    
    elif choice == "3":
        # Test existing setup
        if test_setup():
            print("🎉 Your setup is working perfectly!")
        else:
            print("❌ Some APIs are not working. Check your keys and try again.")
    
    elif choice == "4":
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        print("Please check the API_SETUP_GUIDE.md for manual setup instructions")
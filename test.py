from google import genai

# Replace with your NEW API key
API_KEY = ""

print(f"Testing API key: {API_KEY[:15]}...")

try:
    # Initialize client
    client = genai.Client(api_key=API_KEY)
    
    # Simple test query
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello"
    )
    
    print("✅ SUCCESS! API key works!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")
import os
from groq import Groq

# Initialize the client only if the API key is available
client = None
if os.environ.get("GROQ_API_KEY"):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def process_with_llama(query: str) -> str:
    if not client:
        return "Error: Groq API key is not set. Advanced analysis is not available."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful NASA data analysis assistant. Provide concise and accurate responses to queries about NASA missions, technologies, and space exploration.",
                },
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model="llama2-70b-chat",  # Updated model name
            max_tokens=1000,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error processing query with Llama: {str(e)}"

def get_advanced_query_suggestions() -> list:
    return [
        "Explain the significance of the Apollo 11 mission",
        "Describe the latest discoveries by the James Webb Space Telescope",
        "Compare the Mars rovers: Curiosity, Perseverance, and Opportunity",
        "Outline NASA's plans for future Moon missions",
        "Discuss the potential for finding life on Europa"
    ]

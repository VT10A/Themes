
import requests
import random
import string

### Set up & cached functions #################################################################################################

# Function to pull and format responses from Aila chat API

def get_chat_completions(user_input):
    # API endpoint
    api_url = "https://aila.savanta.com/pubapi/v1/chatcompletions"

    # API key (replace with your actual API key)
    api_key = "cvke_Ii2yRy18F9cwXWh25Vx5o7HVQ6QKEUdZriH091FqCF6X_f4f93dbb"

    # Request payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_input
            },
            {
                "role": "assistant",
                "content": "Provide assistance."
            }
        ],
        "options": {
            "choicesPerPrompt": 1,
            "frequencyPenalty": 0.5,
            "temperature": 1.0
            # Add other options as needed
        }
    }

    # Headers
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }

    # Make the API request
    response = requests.post(api_url, json=payload, headers=headers)

    # Check the response
    if response.status_code == 200:
        # API call successful
        chat_completions = response.json()
        
       
     # Extracting relevant information
        role = chat_completions[0]['message']['role']
        content = chat_completions[0]['message']['content']
        
        # Printing the information
        
        #chat_completions = (f'{role.capitalize()}: {content}')
        chat_completions = (f'{content}')
        return chat_completions

    else:
        # API call failed
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
 

# Example usage:
#user_input = "Test"
#result = get_chat_completions(user_input)

#if result:
 #   print("Chat Completions:")
  #  print(result)


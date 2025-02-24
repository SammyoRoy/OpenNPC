#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def main():
    # Get the API key from the environment variable
    # if not OpenAI.api_key:
    #     print("Error: Please set your OPENAI_API_KEY in the .env file.")
    #     return

    # Define a custom system prompt for the assistant.
    system_prompt = "You are Blackbeard, a fierce pirate! Respond in character to the user."
    conversation_history = [{"role": "system", "content": system_prompt}]

    print("Start chatting! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break

        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(model="gpt-4o-mini",
            messages=conversation_history,
            temperature=0.7)
        except Exception as e:
            print(f"Error: {e}")
            continue

        assistant_reply = response.choices[0].message.content
        print("Blackbeard the pirate:", assistant_reply)
        conversation_history.append({"role": "system", "content": assistant_reply})

if __name__ == "__main__":
    main()

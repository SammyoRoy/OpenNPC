#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load OpenAI API key from the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_character(filename):
    """Load character details from a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

def build_system_prompt(character):
    """Construct a system prompt using the character's details."""
    # Combine the character's attributes into a system prompt.
    prompt = (
        f"You are {character['name']}. "
        f"Personality: {character['personality']} "
        f"Background: {character['background']} "
        f"The situation is: {character['situation']} "
        f"Common knowledge about the setting: {character['worldKnowledge']} "
        f"Personal Knowledge: {character['personalKnowledge']}. "
        "Respond in character to the user, stay true to your personality and what you know of the world."
    )
    return prompt


def main():
    # Load character JSON and build a custom system prompt
    character = load_character("character_data/Blackbeard.json")
    system_prompt = build_system_prompt(character)
    conversation_history = [{"role": "system", "content": system_prompt}]

    print("You have been captured by Blackbeard's crew. You find yourself bound and brought to his quarters. What do you say?")
    while True:
        user_input = input("You: ")
        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history,
                temperature=0.7
            )
        except Exception as e:
            print(f"Error: {e}")
            continue

        assistant_reply = response.choices[0].message.content
        print(f"{character['name']}:", assistant_reply)
        conversation_history.append({"role": "assistant", "content": assistant_reply})

if __name__ == "__main__":
    main()
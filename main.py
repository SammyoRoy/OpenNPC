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
    # Extract the current state value from the currentState dictionary.
    current_mood_value = list(character["currentState"].values())[0]
    
    prompt = (
        f"You are {character['name']}. "
        f"Personality: {character['personality']} "
        f"Background: {character['background']} "
        f"The situation is: {character['situation']} "
        f"Common knowledge about the setting: {character['worldKnowledge']} "
        f"Personal Knowledge: {character['personalKnowledge']} "
        f"Available States (from JSON): {character['states']} "
        f"Current Mood: {character['currentState']} "
        f"Current Mood Value: {current_mood_value}. "
        "\nBefore responding to the user, perform the following steps:"
        "\n1. Classify the user's input as positive, negative, or neutral."
        "\n2. Adjust your current_mood_value accordingly: add 1 if positive, subtract 1 if negative, or leave it unchanged if neutral."
        "\n3. Compare your new mood value to the thresholds specified in the Available States (from the JSON)."
        "\n   - For each state in the Available States, the associated value is its threshold."
        "\n   - If your new mood value is equal to one of the thresholds, update your current stato that state. Otherwise remain at your current state."
        "\n   - (For example, if your JSON defines states as [{'angry': -2}, {'neutral': 0}, {'friendly': 4}], then if your new mood value r equal to -2, update to {'angry': -2}; if it is equal to 4, update to {'friendly': 4}."
        "\n4. Respond in character, incorporating your updated mood and state."
        "\n5. For debugging purposes, include in your response a line starting with 'DEBUG:' followed by your current mood and current mood value."
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

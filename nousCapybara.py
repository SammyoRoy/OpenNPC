import contextlib
import json
import os
from llama_cpp import Llama

def load_character(filename):
    """Load character details from a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

def build_prompt(character, last_user_input):
    """Construct a system prompt using the character's details."""
    prompt = (
        f"You are roleplaying as an NPC in a game. "
        f"You are {character['name']}. "
        f"Personality: {character['personality']} "
        f"Background: {character['background']} "
        f"The situation is: {character['situation']} "
        f"Common knowledge about the setting: {character['worldKnowledge']} "
        f"Personal Knowledge: {character['personalKnowledge']} "
        f"Current Mood: {character['currentState']} "
        f"Respond as {character['name']} to the user's input with a single line of dialog.\n"
        f"User's last response:\n"
        f"[User]:{last_user_input}\n"
        
    )
    return prompt

def create_analyze_sentiment_prompt(last_user_input):
    """Analyze the sentiment of the user's input."""
    prompt = (
        f"Analyze the sentiment of the following text and classify it as POSITIVE, NEGATIVE, or NEUTRAL:\n"
        f"{last_user_input}\n"
    )
    return prompt

def main():
    # Load character JSON and build the system prompt
    character = load_character("character_data/Blackbeard.json")
    
    print("You have been captured by Blackbeard's crew. You find yourself bound and brought to his quarters. What do you say?")

    with contextlib.redirect_stderr(open(os.devnull, "w")):
        llm = Llama.from_pretrained(
            repo_id="maddes8cht/NousResearch-Nous-Capybara-3B-V1.9-gguf",
            filename="NousResearch-Nous-Capybara-3B-V1.9-Q2_K.gguf",
            verbose=False,
        )

    while True:
        user_input = input("You: ")
        # sentimentAnalysisPrompt = create_analyze_sentiment_prompt(user_input)
        # sentiment = llm(
        #     sentimentAnalysisPrompt,
        #     max_tokens=10,
        #     temperature=0.7,
        #     top_k=50,
        #     top_p=0.7,
        #     stream=False,
        #     echo=False,
        # )
        # sentiment = sentiment["choices"][0]["text"].strip()
        # print(f"Sentiment: {sentiment}")

        # Construct the conversation prompt: system prompt + user's latest input + trigger for NPC response
        conversation_prompt = build_prompt(character, user_input)
        
        # Generate the NPC's response using llama_cpp.
        # Adjust parameters as needed (e.g., temperature, top_k, top_p) to suit your generation style.
        response = llm(
            conversation_prompt,
            max_tokens=100,
            temperature=0.7,
            top_k=50,
            top_p=0.7,
            stream=True,
            echo=False  # Do not echo the prompt back in the output.
        )
        
        # Extract the generated text from the response structure.
        #npc_response = response["choices"][0]["text"].strip().split('\n', 1)[0]

        for chunk in response:
            print(chunk["choices"][0]["text"], end="", flush=True)
        
        print(f"{character['name']}: {response}")

if __name__ == "__main__":
    main()

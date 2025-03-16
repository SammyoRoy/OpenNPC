import json
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
        f"[{character['name']}]:"
    )
    return prompt

def main():
    # Load character JSON and build the system prompt
    character = load_character("character_data/Blackbeard.json")
    
    print("You have been captured by Blackbeard's crew. You find yourself bound and brought to his quarters. What do you say?")
    
    # Initialize the Llama model using llama_cpp
    llm = Llama.from_pretrained(
        repo_id="maddes8cht/NousResearch-Nous-Capybara-3B-V1.9-gguf",
        filename="NousResearch-Nous-Capybara-3B-V1.9-Q2_K.gguf",
        verbose=False,
    )
    
    while True:
        user_input = input("You: ")
        # Construct the conversation prompt: system prompt + user's latest input + trigger for NPC response
        conversation_prompt = build_prompt(character, user_input)
        
        # Generate the NPC's response using llama_cpp.
        # Adjust parameters as needed (e.g., temperature, top_k, top_p) to suit your generation style.
        response = llm(
            conversation_prompt,
            max_tokens=300,
            temperature=0.7,
            top_k=50,
            top_p=0.7,
            echo=False  # Do not echo the prompt back in the output.
        )
        
        # Extract the generated text from the response structure.
        npc_response = response["choices"][0]["text"].strip()
        
        print(f"{character['name']}: {npc_response}")

if __name__ == "__main__":
    main()

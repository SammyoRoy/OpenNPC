import json
from transformers import AutoTokenizer
import transformers
import torch

# Model and Tokenizer Initialization
model = "PY007/TinyLlama-1.1B-Chat-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model)

# Pipeline Initialization
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)

def load_character(filename):
    """Load character details from a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

def build_prompt(character):
    """Construct a system prompt using the character's details."""
    
    prompt = (
        f"You are roleplaying as an NPC in a game."
        f"You are {character['name']}. "
        f"Personality: {character['personality']} "
        f"Background: {character['background']} "
        f"The situation is: {character['situation']} "
        f"Common knowledge about the setting: {character['worldKnowledge']} "
        f"Personal Knowledge: {character['personalKnowledge']} "
        f"Current Mood: {character['currentState']} "
        f"Respond in character to the user's input with a single line of dialog.\n"
        f"User's last input:\n"
    )
    return prompt

def main():
    # Load character JSON and build a custom system prompt
    character = load_character("character_data/Blackbeard.json")
    system_prompt = build_prompt(character)

    print("You have been captured by Blackbeard's crew. You find yourself bound and brought to his quarters. What do you say?")
    # Initialize the conversation history with the system prompt
    conversation_history = system_prompt

    while True:
        user_input = input("You: ")
        # Append the user's input to the conversation history
        # Prepare the prompt for generation by adding the character's name as the responder
        conversation_prompt = system_prompt+user_input + "\n"
        print(conversation_prompt)
        
        # Generate the NPC's response
        sequences = pipeline(
            conversation_prompt,
            do_sample=True,
            top_k=50,
            top_p=0.7,
            num_return_sequences=1,
            repetition_penalty=1.1,
            max_new_tokens=100,
        )
        # The generated text includes the prompt, so we extract only the new response
        generated_text = sequences[0]["generated_text"]
        npc_response = generated_text[len(conversation_prompt):].strip()
        
        # Append the NPC's response to the conversation history
        conversation_history += f"\n{character['name']}: {npc_response}"
        print(f"{character['name']}: {npc_response}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from openai import OpenAI
from opennpc import OpenNPC
from opennpc import load_character
        
def main():
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    character = load_character("character_data/Blackbeard.json")
    pirate_NPC = OpenNPC(client, character)
    pirate_NPC.start_converstation()
    while(True):
      while(True):
        user_input = input("You: ")
        if user_input:
          break
      message, think, stats = pirate_NPC.continue_converstion(user_input)
      # print(think)
      print(f"{character['name']}:", message)
      print(stats)
      terminate, events = pirate_NPC.event_listener(stats)
      if terminate:
        pirate_NPC.end_converstion()
        return
    
if __name__ == "__main__":
    main()

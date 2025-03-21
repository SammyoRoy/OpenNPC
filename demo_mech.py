#!/usr/bin/env python3
from openai import OpenAI
from opennpc import OpenNPC
from opennpc import load_character
import json
        
def main():
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    character = load_character("character_data/Nova.json")
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
        break
    
    with open("character_data/Nova.json", "r") as f:
        character_data = json.load(f)
    
    for id in events:
      match id:
        case 24341002:
          print("Relation with nova is now hostile")
          character_data['mood-currentState'] = "hostile"
          character_data['mood-currentStateValue'] = -2
        case 24341001:
          print("Relation with nova is now unkind")
          character_data['mood-currentState'] = "unkind"
          character_data['mood-currentStateValue'] = -1
        case 24340000:
          print("Relation with nova is now neutral")
          character_data['mood-currentState'] = "neutral"
          character_data['mood-currentStateValue'] = 0
        case 24340001:
          print("Relation with nova is now recognized")
          character_data['mood-currentState'] = "recognized"
          character_data['mood-currentStateValue'] = 1
        case 24340002:
          print("Relation with nova is now friendly")
          character_data['mood-currentState'] = "friendly"
          character_data['mood-currentStateValue'] = 2
        case 24340003:
          print("Relation with nova is now trusted")
          character_data['mood-currentState'] = "trusted"
          character_data['mood-currentStateValue'] = 3
        case 24340004:
          print("Relation with nova is now respected")
          character_data['mood-currentState'] = "respected"
          character_data['mood-currentStateValue'] = 4
        case 24340005:
          print("Relation with nova is now honored")
          character_data['mood-currentState'] = "honored"
          character_data['mood-currentStateValue'] = 5
        case 24340006:
          print("Relation with nova is now sworn")
          character_data['mood-currentState'] = "sworn"
          character_data['mood-currentStateValue'] = 6
        case 24340007:
          print("Relation with nova is now bloodsworn")
          character_data['mood-currentState'] = "bloodsworn"
          character_data['mood-currentStateValue'] = 7
        case 24341111:
          print("Relation with nova has beew reset")
          character_data['mood-currentState'] = "neutral"
          character_data['mood-currentStateValue'] = 0
      
      with open("character_data/Nova.json", 'w') as f:
        json.dump(character_data, f, indent=4)
    
if __name__ == "__main__":
    main()

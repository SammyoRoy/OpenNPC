import sys
import time
import json
from collections import OrderedDict
from openai import OpenAI

def load_character(filename):
    """Load character details from a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

def build_system_prompt(character):
    """Construct a system prompt using the character's details."""
    
    prompt = (
        f"You are {character['name']}. "
        f"Personality: {character['personality']} "
        f"Background: {character['background']} "
        f"The situation is: {character['situation']} "
        f"Common knowledge about the setting: {character['worldKnowledge']} "
        f"Personal Knowledge: {character['personalKnowledge']} "
        f"[Available Mood States] = {character['mood-states']} "
        f"[Current Mood State] = {character['mood-currentState']} "
        f"[Current Mood Evaluation] = {character['mood-currentStateValue']}. "
        "\nWords enclose between [ and ] means it repersents a variable"
        "\nBefore responding to the user, perform the following steps:"
        "\n1. Classify the user's input as positive, negative, or neutral."
        "\n2. Update your [Current Mood Evaluation] accordingly: add 1 if positive, subtract 1 if negative, or leave it unchanged if neutral."
        "\n   - [Current Mood Evaluation] is a integer value evaluating mood"
        "\n   - The updated [Current Mood Evaluation] is the new [Current Mood Evaluation] that should be refered to in later conversations"
        "\n3. Compare your new [Current Mood Evaluation] to the threshold values specified in the [Available Mood States]"
        "\n   - If your new [Current Mood Evaluation] is equal to one of the [Mood Evaluation Threshold], update your [Current Mood] to the matching [Mood State] in [Available Mood States]. Otherwise do not update."
        "\n   - [Current Mood State] is a string value classifying mood"
        "\n   - [Available Mood States] is formated as a JSON Collection of { [Mood State]: [Mood Evaluation Threshold] }"
        "\n   - [Mood State] is a string value classifying mood for [Current Mood State] to match"
        "\n   - [Mood Evaluation Threshold] is a integer value evaluating mood for [Current Mood Evaluation] to compare with"
        "\nWhen responding to the user perform the following:"
        "\n   - Respond in character, incorporating your [Current Mood State]"
        "\n   - Limit your respond with only conversations. Ignore narration."
        "\n   - Generate you respond to user in plain text without any special format"
        "\n   - Enclose the message between 2 tags <message> and </message>, each tag takes a seperate line"
        "\nAppend a statistic message at the end of your response"
        "\n   - Enclose the message between 2 tags <stats> and </stats>, each tag takes a seperate line"
        "\n   - Print only the value of the variables enclosed between [ and ] and do NOT print the name of the variable enclosed between [ and ]"
        "\nGenerate the statistic message in following format:"
        "\n   - { [Current Mood State]: [Current Mood Evaluation] }"
    )
    return prompt

def extract_string(text, start_tag, end_tag):
  try:
    start_index = text.rindex(start_tag) + len(start_tag)
    end_index = text.rindex(end_tag, start_index)
    return text[start_index:end_index].strip()
  except ValueError:
    return None

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
          
          
          
class OpenNPC:
    
    def __init__(self, client:OpenAI, character, model="qwq-32b", temperature=0.6, top_p=0.95):
        self.character = character 
        self.client = client
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        system_prompt = build_system_prompt(self.character)
        self.conversation_history = [{"role": "system", "content": system_prompt}]
        self.openning_message = self.character['openningMessage']
        self.user_conversation = []
        self.npc_conversation = []
    
    def start_converstation(self):
        eprint("[stderr] start_converstation() called")
        print(self.openning_message)
        
    def continue_converstion(self, user_input):
        eprint("[stderr] continue_converstion() called")
        conversation_history_temp = self.conversation_history.copy()
        conversation_history_temp.append({"role": "user", "content": user_input})
        start_time = time.perf_counter()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                top_p=self.top_p,
                messages=conversation_history_temp
            )
        except Exception as e:
            return e
        end_time = time.perf_counter()
        time_gen = end_time - start_time
        eprint("[stderr]", time_gen, "secs")
        eprint("[stderr]", response.usage.completion_tokens / (time_gen), "tok/sec")
        
        assistant_reply = response.choices[0].message.content
        
        think = extract_string(assistant_reply, "<think>", "</think>")
        if (think is None):
            eprint("[stderr] extract_string(): 'think' failed, retrying converstaion.")
            return self.continue_converstion(user_input)
        message = extract_string(assistant_reply, "<message>", "</message>")
        if (message is None):
            eprint("[stderr] extract_string(): 'message' failed, retrying converstaion.")
            return self.continue_converstion(user_input)
        stats = extract_string(assistant_reply, "<stats>", "</stats>")
        if (stats is None):
            eprint("[stderr] extract_string(): 'stats' failed, retrying converstaion.")
            return self.continue_converstion(user_input)
        
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        self.user_conversation.append({"role": "user", "content": user_input})
        self.npc_conversation.append({"role": "assistant", "content": assistant_reply})
        
        return message, think, stats
    
    def end_converstion(self):
        eprint("[stderr] end_converstation() called")
        
    def event_listener(self, stats):
        eprint("[stderr] event_listener() called")
        triggered_events = []
        for event in self.character['events']:
            if any(ct in stats for ct in event['condition']) and any(ct in str(self.user_conversation) for ct in event['user-trigger']) and any(ct in str(self.npc_conversation) for ct in event['npc-trigger']):
                eprint("[stderr]", event['event'], "triggered")
                triggered_events.append(event['id'])
                print(event['narration'])
                if event['terminate']:
                    return True, triggered_events
        return False, triggered_events

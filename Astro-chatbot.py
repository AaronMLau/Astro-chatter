# Astro-chatter
# A question-answering chatbot exploring the cosmos
# 
# To run this bot, open a terminal with python 3.8+ 
# and type: python3 Astro-chatbot.py
# 
# To read more documentation on this bot, check out 
# the Github page: 
#
# =========================================================================================================

# Using only a few libraries
import re
from collections import defaultdict

dst = defaultdict(list)

# nlu(input): Interprets a natural language input and identifies relevant slots and their values
# Input: A string of text.
# Returns: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is most
#          appropriate for the corresponding slot.  If no slot values are extracted, the function should
#          return an empty list.
def nlu(input=""):
    # [YOUR CODE HERE]
    
    # Dummy code for sample output (delete or comment out when writing your code!):
    slots_and_values = []
    
    # To narrow the set of expected slots, you may (optionally) first want to determine the user's intent,
    # based on what the chatbot said most recently.
    user_intent = ""
    if "dialogue_state_history" in dst:
        if dst["dialogue_state_history"][0] == "request_size":
            # Check to see if the input contains a valid size.
            pattern = re.compile(r"\b([Ss]mall)|([Mm]edium)|([Ll]arge)\b")
            match = re.search(pattern, input)
            if match:
                user_intent = "respond_size"
                slots_and_values.append(("user_intent_history", ["respond_size"]))
            else:
                user_intent = "unknown"
                slots_and_values.append(("user_intent_history", ["unknown"]))
        else:
            # Check to see if the user entered "yes" or "no."
            yes_pattern = re.compile(r"\b([Yy]es)|([Yy]eah)|([Ss]ure)|([Oo][Kk](ay)?)\b")
            match = re.search(yes_pattern, input)
            if match:
                user_intent = "respond_yes"
                slots_and_values.append(("user_intent_history", ["respond_yes"]))
            else:
                no_pattern = re.compile(r"\b([Nn]o(pe)?)|([Nn]ah)\b")
                match = re.search(no_pattern, input)
                if match:
                    user_intent = "respond_no"
                    slots_and_values.append(("user_intent_history", ["respond_no"]))
                else:
                    user_intent = "unknown"
                    slots_and_values.append(("user_intent_history", ["unknown"]))
            
    # If you're maintaining a dialogue state history but there's nothing there yet, this is probably the
    # first input of the conversation!
    else:
        user_intent = "greeting"
        slots_and_values.append(("user_intent_history", ["greeting"]))
        
    # Then, based on what type of user intent you think the user had, you can determine which slot values
    # to try to extract.
    if user_intent == "respond_size":
        # In our sample chatbot, there's only one slot value we'd want to extract if we thought the user
        # was responding with a pizza size.
        pattern = re.compile(r"\b[Ss]mall\b")
        contains_small = re.search(pattern, input)
        
        pattern = re.compile(r"\b[Mm]edium\b")
        contains_medium = re.search(pattern, input)
        
        pattern = re.compile(r"\b[Ll]arge\b")
        contains_large = re.search(pattern, input)
        
        # Note that this if/else block wouldn't work perfectly if the input contained, e.g., both "small"
        # and "medium" ... ;)
        if contains_small:
            slots_and_values.append(("pizza_size", "small"))
        elif contains_medium:
            slots_and_values.append(("pizza_size", "medium"))
        elif contains_large:
            slots_and_values.append(("pizza_size", "large"))
        
    return slots_and_values


# update_dst(input): Updates the dialogue state tracker
# Input: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is
#        most appropriate for the corresponding slot.  Defaults to an empty list.
# Returns: Nothing
def update_dst(input=[]):
    global dst
    for slot, value in input:
        if slot in dst and isinstance(dst[slot], list):
            if isinstance(value, list):
                for val in value:
                    dst[slot].insert(0, val)
            else:
                dst[slot].insert(0, value)
        else:
            dst[slot] = value
    return

# get_dst(slot): Retrieves the stored value for the specified slot, or the full dialogue state at the
#                current time if no argument is provided.
# Input: A string value corresponding to a slot name.
# Returns: A dictionary representation of the full dialogue state (if no slot name is provided), or the
#          value corresponding to the specified slot.
def get_dst(slot=""):
    global dst
    if slot != "":
        try:
            return dst[slot]
        except KeyError as ERR:
            pass
    return dst


# dialogue_policy(dst): Selects the next dialogue state to be uttered by the chatbot.
# Input: A dictionary representation of a full dialogue state.
# Returns: A string value corresponding to a dialogue state, and a list of (slot, value) pairs necessary
#          for generating an utterance for that dialogue state (or an empty list if no (slot, value) pairs
#          are needed).

# TODO: Look into user intents/slot values
#https://discover.bot/bot-talk/define-and-design-intents-for-your-bot/
def dialogue_policy(dst=[]):
    next_state = "greetings"
    slot_values = []
    
    if len(dst) == 0:
        next_state = "greetings"
    elif dst["dialogue_state_history"][0] == "greetings":
        next_state = "question"
    elif dst["dialogue_state_history"][0] == "question" and dst["user_intent_history"][0] == "question":
        next_state = "thinking"
    elif dst["dialogue_state_history"][0] == "question" and dst["user_intent_history"][0] == "statement":
        next_state = "check_correctness"
        # slot values here will re-state the statement and then determine if it is true/false with the same lookup as a question
        # type: string
        slot_values = []
    elif dst["dialogue_state_history"][0] == "question" and dst["user_intent_history"][0] == "unknown":
        next_state = "off_topic"
        # slot values here will ask for clarification and restate what the user said
        # type: string
        slot_values = []
    elif dst["dialogue_state_history"][0] == "thinking":
        next_state = "answer"
    elif dst["dialogue_state_history"][0] == "answer" or dst["dialogue_state_history"][0] == "check_correctness" or dst["dialogue_state_history"][0] == "off_topic" and dst["user_intent_history"][0] == "more_info":
        next_state = "sources"
        # slot values here will be the sources, with a snippet about each one
        # type: list of strings
        slot_values = [] 
    elif dst["dialogue_state_history"][0] == "answer" or dst["dialogue_state_history"][0] == "check_correctness" or dst["dialogue_state_history"][0] == "off_topic" and dst["user_intent_history"][0] == "thanks":
        next_state = "terminate"
    elif dst["dialogue_state_history"][0] == "answer" or dst["dialogue_state_history"][0] == "check_correctness" or dst["dialogue_state_history"][0] == "off_topic":
        next_state = "question"
    else:
        pass
    
    update_dst([("dialogue_state_history", [next_state])])
    return next_state, slot_values
	
# nlg(state, slots=[]): Generates a surface realization for the specified dialogue act.
# Input: A string indicating a valid state, and optionally a list of (slot, value) tuples.
# Returns: A string representing a sentence generated for the specified state, optionally
#          including the specified slot values if they are needed by the template.
def nlg(state, slots=[]):
    # [YOUR CODE HERE]
    
    # Dummy code for sample output (delete or comment out when writing your code!):
    templates = defaultdict(list)
    
    # Build at least two templates for each dialogue state that your chatbot might use.
    templates["greetings"] = []
    templates["greetings"].append("Hi, welcome to 421Pizza!  Would you like to order a pizza?")
    
    templates["clarification"] = []
    templates["clarification"].append("Just double-checking ...did you say that you want <num_pizzas> pizzas?")
    
    templates["repeat"] = []
    templates["repeat"].append("I'm sorry, I didn't understand what you said.  Can you answer my original question in a way that I might understand it better?")
    
    templates["terminate"] = []
    templates["terminate"].append("Okay, it was great chatting with you.  Have a nice day!")
    
    # When you implement this for real, you'll need to randomly select one of the templates for
    # the specified state, rather than always selecting template 0.  You probably also will not
    # want to rely on hardcoded input slot positions (e.g., slots[0][1]).  Optionally, you might
    # want to include logic that handles a/an and singular/plural terms, to make your chatbot's
    # output more natural (e.g., avoiding "did you say you want 1 pizzas?").
    output = ""
    if len(slots) > 0:
        output = templates[state][0].replace("<num_pizzas>", str(slots[0][1]))
    else:
        output = templates[state][0]
    return output



# Use this main function to test your code when running it from a terminal
# Sample code is provided to assist with the assignment, feel free to change/remove it if you want
# You can run the code from terminal as: python3 chatbot.py

def main():
    
    # You can choose whether your chatbot or the participant will make the first dialogue utterance.
    # In the sample here, the chatbot makes the first utterance.
    current_state_tracker = get_dst()
    next_state, slot_values = dialogue_policy(current_state_tracker)
    output = nlg(next_state, slot_values)
    print(output)
    
    # With our first utterance complete, we'll enter a loop for the rest of the dialogue.  In some cases,
    # especially if the participant makes the first utterance, you can enter this loop directly without
    # needing the previous code block.
    while next_state != "terminate":
        # Accept the user's input.
        user_input = input()
        
        # Perform natural language understanding on the user's input.
        slots_and_values = nlu(user_input)
        
        # Store the extracted slots and values in the dialogue state tracker.
        update_dst(slots_and_values)
        
        # Get the full contents of the dialogue state tracker at this time.
        current_state_tracker = get_dst()
        
        # Determine which state the chatbot should enter next.
        next_state, slot_values = dialogue_policy(current_state_tracker)
        
        # Generate a natural language realization for the specified state and slot values.
        output = nlg(next_state, slot_values)
        
        # Print the output to the terminal.
        print(output)
        


################ Do not make any changes below this line ################
if __name__ == '__main__':
    main()

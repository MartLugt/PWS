text = input().lower()

# Must return the intent with the most confidence and its confidence.
# Very crude and simple...

def parse(text):
    # Making a dictionary of intents, which are lists of all its keywords.
    intents = {"get_time": ["time", "get", "what", "test"],
               "set_time": ["time", "set", "change"],
               "get_mood": ["how", "mood", "you", "what"]
               }

    confidences = {}

    # Calculate percentage of keywords
    for intent in intents:
        # populate confidence list.
        confidences[intent] = 0.0
        for keyword in intents[intent]:
            if keyword in text:
                confidences[intent] += 1/len(intents[intent])

    # Calculate total confidence
    total_confidence = 0
    for confidence in confidences.values():
        total_confidence += confidence

    if total_confidence == 0:
        print("no match")
        exit(0)

    # Make confidence 1 total.
    for intent in confidences:
        confidences[intent] = confidences[intent]/total_confidence

    # Get key with max value
    return max(confidences, key=confidences.get), max(confidences.values())


print(parse(text))

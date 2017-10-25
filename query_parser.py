text = input().lower()

# Must return the intent with the most confidence and its confidence.
# Very crude and simple...

# PROBLEM: any time how or any other keyword is said, the query parser will find a match.
# there should be keywords that NEED to be in the sentence to get a match.
# Keywords should be ranked.

def parse(text):
    # Making a dictionary of intents, which are lists of all its keywords.
    intents = {"get_time": {"time": 0, "what": 1, "get": 2},
               "set_time": {"time": 0, "set": 1, "change": 2},
               "get_mood": {"mood": 1, "how are you": 1},
               }

    confidences = {}

    # Calculate percentage of keywords
    for intent in intents:
        # populate confidence list.
        confidences[intent]= 0.0
        for keyword in intents[intent]:
            if keyword in text:
                confidences[intent] += 0
            elif intents[intent][keyword] == 0:
                confidences[intent] = 0
                break

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
print(parse(text))

text = "What's the time?".lower()


def get_max(dic):
    max_value = max(dic.values())
    max_keys = [k for k, v in dic.items() if v == max_value]
    return max_value, max_keys


# Need to make a tuple/list with the intent and confidence OR dictionary of all intents with their confidence
intents = {"time_get": 0, "time_set": 0}

if "time" in text:
    # bad way to do it, intents with more keywords are now more likely.
    # Confidence should be percentage. Total sum of all confidences should be 1 or 100.
    if "what" in text or "get" in text:
        intents["time_get"] += 1
    if "set" in text:
        intents["time_set"] += 1

print(get_max(intents))

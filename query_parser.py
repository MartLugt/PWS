# Must return the intent with the most confidence and its confidence.
# Very crude and simple...


def parse(text):
    # Making a dictionary of intents, which are lists of all its keywords.
    # need to add this or that for keywords ea what or get
    # The intents higher up in the dictionary are more important and will be picked faster.
    intents = {"search": {"search": 0},
               "get_time": {"time": 0, "what": 2, "get": 2},
               "get_mood": {"mood": 1, "how are you": 1},
               "joke": {"joke": 0},
               "get_weather": {"weather": 1, "forecast":1},
               "get_news": {"news": 0, "BBC": 1, "sport": 2, "tech": 2, "business": 2},
               "calendar": {"event": 2, "calendar": 1},
               "snowboy": {"snowboy": 1, "name": 2},
               "guess": {"guess": 0, "play": 1, "number": 1},
               "make_note": {"note": 0, "make": 0},
               "get_note": {"notes": 1, "note": 1, "get": 0},
               "urmom": {"your": 1, "mom": 1, "gay": 0},
               "change_voice": {"change": 0, "voice": 0},
               "echo": {"echo": 0},
               "stop": {"stop": 1, "shutdown": 1}
               }

    confidences = {}

    # Calculate percentage of keywords
    for intent in intents:
        # populate confidence list.
        confidences[intent]= 0

        print("\n" + intent)

        points = 0  # TODO: better names
        matches = 0
        zero_keywords = 0
        print(zero_keywords)
        keyword_buffer = []
        print(keyword_buffer)

        for keyword in intents[intent]:
            print(intent, keyword)
            if keyword in text and keyword not in keyword_buffer:
                points += intents[intent][keyword]
                matches += 1
                keyword_buffer.append(keyword)

            if intents[intent][keyword] == 0:
                zero_keywords += 1
        print("keywords with 0:", str(zero_keywords))

        if matches == 1 and points == 0:  # another weird shadow case
            confidences[intent] = 1.0
        elif matches == 0:
            confidences[intent] = 0
        else:
            confidences[intent] = points / matches

        zeroes = 0
        for word in keyword_buffer:
            print(word, intents[intent][word])
            if intents[intent][word] == 0:
                zeroes += 1
        print("zeroes:", str(zeroes))

        if zeroes != zero_keywords:
            confidences.pop(intent, None)

        if zero_keywords == 0 and points == 0:
            confidences.pop(intent, None)

    print(confidences)
    print("\n\n")
    if confidences:
        return min(confidences, key=confidences.get), min(confidences.values())
    else:
        return "no_match", 0.0

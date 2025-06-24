import spacy

nlp = spacy.load("en_core_web_sm")

def tokenize_input(text):
    doc = nlp(text)
    return [token.text for token in doc]

def parse_tokens(tokens):
    return parse_with_spacy(" ".join(tokens))

def parse_with_spacy(text):
    doc = nlp(text)
    commands = []

    text_lower = text.lower()

    # Detect function with math operation
    if "function" in text_lower:
        if "add" in text_lower:
            commands.append({"type": "function", "name": "add_numbers", "params": ["a", "b"], "operation": "add"})
        elif "multiply" in text_lower:
            commands.append({"type": "function", "name": "multiply_numbers", "params": ["a", "b"], "operation": "multiply"})
        elif "subtract" in text_lower:
            commands.append({"type": "function", "name": "subtract_numbers", "params": ["a", "b"], "operation": "subtract"})
        elif "divide" in text_lower:
            commands.append({"type": "function", "name": "divide_numbers", "params": ["a", "b"], "operation": "divide"})
        else:
            # extract verb+noun to name function
            verb = ""
            noun = ""
            for token in doc:
                if token.pos_ == "VERB":
                    verb = token.lemma_
                if token.pos_ == "NOUN":
                    noun = token.lemma_
            name = f"{verb}_{noun}" if verb and noun else "unnamed_function"
            commands.append({"type": "function", "name": name})

    # Variable assignment
    if "variable" in text_lower and "as" in text_lower:
        for i, token in enumerate(doc):
            if token.text.lower() == "variable":
                name = doc[i + 1].text
            if token.text.lower() == "as":
                value = doc[i + 1].text
        commands.append({"type": "variable", "name": name, "value": value})

    # Loop detection
    if "loop" in text_lower and "from" in text_lower and "to" in text_lower:
        start = None
        end = None
        for i, token in enumerate(doc):
            if token.text.lower() == "from":
                start = int(doc[i + 1].text)
            if token.text.lower() == "to":
                end = int(doc[i + 1].text)
        if start is not None and end is not None:
            commands.append({"type": "loop", "start": start, "end": end})

    # Conditional
    if "if" in text_lower and "greater" in text_lower and "than" in text_lower:
        var = None
        val = None
        for i, token in enumerate(doc):
            if token.text.lower() == "if":
                var = doc[i + 1].text
            if token.text.lower() == "than":
                val = doc[i + 1].text
        if var and val:
            commands.append({"type": "if", "var": var, "cond": ">", "value": val})

    return commands
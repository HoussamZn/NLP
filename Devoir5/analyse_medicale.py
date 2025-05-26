import re
def extraire_medicaments_posologie(nlp,texte):
    doc = nlp(texte)
    resultats = []

    pattern_poso = re.compile(r"(\d+mg|\d+g|\d+mcg|\d+ml)[^\.\,]*")

    for i, token in enumerate(doc):
        # Cherche les médicaments : noms après "de", "du", "l'", etc.
        if token.pos_ == "NOUN" and token.text.lower() in ["amoxicilline", "paracétamol", "ciprofloxacine"]:
            # Cherche à droite la posologie dans le texte brut
            span_text = doc[i:i+6].text  # max 6 tokens à droite
            match = pattern_poso.search(span_text)
            if match:
                resultats.append((token.text, match.group()))

    return resultats


def extraire_relations(text:str,nlp):
    doc = nlp(text)
    relations = []
    for token in doc:
        if token.pos_ == "VERB":
            sujet = None
            objet = None
            for child in token.children:
                if child.dep_ in ("nsubj", "nsubj:pass"):
                    sujet = child.text
                elif child.dep_ in ("obj", "obl:arg"):
                    objet = child.text
                    
            if sujet and objet:
                relations.append((sujet, token.lemma_, objet))
        if token.text.lower() in ["raison", "cause", "motif"]:
            head = token.head
            cc_obj = [child for child in token.children if child.dep_ in ["nmod", "fixed", "det", "amod", "obl"]]
            for child in cc_obj:
                if head.dep_ == "ROOT":
                    relations.append((child.text.lower(), token.text.lower(), head.lemma_))
    return relations
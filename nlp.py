import spacy
import re

nlp = spacy.load("en_core_web_md")

relation_keywords = {
    "affiliated-sub-entity": ["affiliated", "related entity"],
    "raw-material-supplier": ["supplier", "supply", "raw material"],
    "it-service-provider": ["IT service", "managed IT", "backup"],
    "legal-service": ["legal", "contract consultation"],
    "accounting-service": ["accounting", "invoice"],
    "insurance-provider": ["insurance", "coverage"]
}

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_org_entities(doc):
    orgs = set()
    for ent in doc.ents:
        if ent.label_ == "ORG":
            orgs.add(ent.text.strip())
    # print("orgs:",list(orgs))
    return list(orgs)

def detect_relation(sentence_text):
    lower = sentence_text.lower()
    print("sentence_text:",lower)
    for rel_type, keywords in relation_keywords.items():
        for kw in keywords:
            if kw in lower:
                return rel_type
    return None

def nlp_pipeline(raw_text):
    clean = clean_text(raw_text)
    doc = nlp(clean)

    triples = []
    for sent in doc.sents:
        sent_text = sent.text

        orgs = extract_org_entities(nlp(sent_text))
        if len(orgs) >= 2:
            # print("orgs:", orgs)
            rel = detect_relation(sent_text)
            
            if rel:
                for org in orgs[1:]:
                    triples.append((orgs[0], rel, org))

    return triples
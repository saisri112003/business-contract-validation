import spacy

nlp = spacy.load("en_core_web_sm")

def extract_details(text):
        doc = nlp(text)
        entities = []
        for ent in doc.ents:
                entities.append([ent.text, ent.label_])
        return entities

if __name__=="__main__":
        text = "Either party may terminate this contract with 32 days written notice to the other party. In the event of termination, Spencer PLC will be compensated for all services performed up to the date of termination."
        print(extract_details(text))
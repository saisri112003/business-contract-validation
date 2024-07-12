from typing import List
import joblib
import nltk
nltk.download('punkt')

def w2f(sent, i):
    word:str = sent[i][0]
    features = {
        'bias':1.0,
        'word.lower()':word.lower(),
        'word[-3:]':word[-3:],
        'word[-2:]':word[-2:],
        'word.isupper()':word.isupper(),
        'word.istitle()':word.istitle(),
        'word.isdigit()':word.isdigit()
    }
    if i>0:
        word1:str = sent[i-1][0]
        features.update({
            '-1:word.lower()':word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True


    if i < len(sent)-1:
        word1:str = sent[i+1][0]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
        })
    else:
        features['EOS'] = True

    return features


nlp = joblib.load("crf_ner_model_v1.pkl")


def extract_entities(text):
    tokens = nltk.word_tokenize(text)
    token_features = [w2f([(token, "O") for token in tokens], i) for i in range(len(tokens))]
    y_pred = nlp.predict_single(token_features)

    
    entities = []
    isOExist = False
    for token, label in zip(tokens, y_pred):
        if label == "O":
            isOExist = True
            continue
    

        elif isOExist == False and len(entities) > 0 and label == entities[-1][1]:
            if token == ",":
                entities[-1][0] += f"{token}"
            else:
                entities[-1][0] += f" {token}"

            continue

        entities.append([token, label])
        isOExist = False

    return entities



if __name__ == "__main__":
    # Example text for extraction
    example_text = """Cole LLC agrees to provide the following services to Hines, Munoz and Dennis. Services are service1, service2, service3.
    Hines, Munoz and Dennis agrees to pay Cole LLC the amount of $36777 for the services described above. Payment shall be made within 66 days of receiving an invoice from Cole LLC.
    This contract will commence on 2024-03-01 and will continue until 2024-01-17 unless terminated earlier in accordance with the Termination clause.
    Both parties agree to maintain the confidentiality of any proprietary or confidential information disclosed during the term of this contract. This obligation will continue beyond the termination of this contract.
    Either party may terminate this contract with 66 days written notice to the other party. In the event of termination, Cole LLC will be compensated for all services performed up to the date of termination.
    This contract shall be governed by and construed in accordance with the laws of the State of Nebraska.
    Cole LLC
    Hines, Munoz and Dennis"""
    
    for line in example_text.splitlines():
        extracted_details = extract_entities(line)
        print(extracted_details)
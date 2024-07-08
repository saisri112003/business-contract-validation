from transformers import BertForSequenceClassification, BertTokenizer
import torch


model_load_path = "./fine_tuned_bert"
model = BertForSequenceClassification.from_pretrained(model_load_path)
tokenizer = BertTokenizer.from_pretrained(model_load_path)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

def predict(text):
    # Tokenize the input text
    inputs = tokenizer(text, truncation=True, max_length=128, return_tensors='pt', padding=True)

    # Move inputs to GPU if available
    inputs = {key:val.to(device) for key, val in inputs.items()}

    # Perform inference 
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1)
        return predicted_class.item()
    
if __name__=="__main__":
        
    # Example text for inference
    example_text = "Cole LLC agrees to provide the following services to Hines, Munoz and Dennis. services are service1 service2, service3."
    predicted_class = predict(example_text)
    print(f"Predicted class: {predicted_class}")



    

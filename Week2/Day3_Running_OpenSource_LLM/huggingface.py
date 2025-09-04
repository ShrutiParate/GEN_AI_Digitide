from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load pre-trained sentiment analysis model
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Create pipeline
nlp_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

#sentimental analysis
# Test sentences
test_sentences = [
    "I love my new phone!",
    "This food tastes terrible.",
    "The movie was fantastic and lovely"
]

# Run predictions
for sentence in test_sentences:
    result = nlp_pipeline(sentence)[0]
    print(f"Input: {sentence}")
    print(f"Prediction: {result['label']} (score: {result['score']:.4f})")
    print("-" * 50)



#text summarization
print("\n=== Text Summarization ===")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")

long_text = """
Artificial Intelligence (AI) is a branch of computer science that aims to create machines that 
can perform tasks that normally require human intelligence. These tasks include learning, 
reasoning, problem-solving, perception, and language understanding. AI is widely used in 
applications such as self-driving cars, virtual assistants, recommendation systems, and medical diagnosis.
"""

summary = summarizer(long_text, max_length=50, min_length=25, do_sample=False)
print("Original Text:", long_text)
print("\nSummary:", summary[0]['summary_text'])



#Text Classifictaion
print("\n=== Text Classification ===")
classifier = pipeline("zero-shot-classification", model="cross-encoder/nli-distilroberta-base")

candidate_labels = ["technology", "sports", "politics", "education"]

text_to_classify = "The government passed a new law to improve the education system."
classification = classifier(text_to_classify, candidate_labels)

print("Input:", text_to_classify)
print("Predicted Label:", classification['labels'][0])
print("Scores:", classification['scores'])


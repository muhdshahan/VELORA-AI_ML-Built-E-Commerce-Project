from transformers import pipeline

# cardiffnlp/twitter-roberta-base-sentiment-latest
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def analyze_sentiment(text: str):
    """
    Returns 'POSITIVE', 'NEGATIVE' for input text.
    """
    if not text.strip():
        return "NEUTRAL"
    result = sentiment_pipeline(text[:512]) # limit to model input size
    return result[0]['label'].upper()  # 'POSITIVE' or 'NEGATIVE'

if __name__ == "__main__":
    # Test
    test_text = input("input:")
    sentiment = analyze_sentiment(test_text)
    print("Sentiment:", sentiment)

    # Evaluation
    eval_texts = [
        ("I love this!", "POSITIVE"),
        ("This is terrible.", "NEGATIVE"),
        ("Not bad, not great.", "NEUTRAL"),
        ("Absolutely wonderful experience", "POSITIVE"),
        ("Worst service ever.", "NEGATIVE"),
        ("Your website looks good having a good interface", "POSITIVE"),
        ("You should really look into the payment part as I faced many issues there, it was better I didnt order", "NEGATIVE"),
        ("You could have created a better website", "NEGATIVE"),
        ("I really like this, I will be sharing it to other people too", "POSITIVE"),
        ("It is best you give up with this as its worst of time", "NEGATIVE"),
        ("Really helpful support team, resolved my issue quickly.", "POSITIVE"),
        ("I waited for hours and nobody responded to my query.", "NEGATIVE"),
        ("The checkout process was fast and simple.", "POSITIVE"),
        ("I'm disappointed with the product quality.", "NEGATIVE"),
        ("Amazing deals! I'll definitely come back for more.", "POSITIVE"),
        ("The website kept crashing every time I tried to order.", "NEGATIVE"),
        ("Effortlessly found everything I needed, thank you!", "POSITIVE"),
        ("The instructions were confusing and unclear.", "NEGATIVE"),
        ("I'm satisfied overall, but delivery was slow.", "NEGATIVE"),
        ("Excellent design and easy navigation!", "POSITIVE")
    ]
    correct = 0
    total = len(eval_texts)
    print("\n Running evaluation:")
    for text, label in eval_texts:
        pred = analyze_sentiment(text)
        print(f"Text: {text} | Prediction: {pred} | Actual: {label}")
        if pred==label:
            correct += 1
    acc = correct / total * 100
    print(f"\n Accuracy: {correct}/{total} ({acc:.1f}%)")
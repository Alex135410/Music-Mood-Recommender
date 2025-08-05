import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset with semicolon delimiter
df = pd.read_csv('../data/emotion.csv', sep=';', header=None, names=['text', 'label'])

# Print first rows and label distribution to verify loading
print("Sample data:")
print(df.head())
print("\nLabel distribution:")
print(df['label'].value_counts())

# Drop rows with missing values (if any)
df = df.dropna()

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# Create pipeline: TF-IDF vectorizer + Logistic Regression classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(max_iter=1000))
])

# Train the model
pipeline.fit(df['text'], df['label'])

# Save the trained model
joblib.dump(pipeline, 'mood_classifier.pkl')


print("\n✅ Model trained and saved as 'mood_classifier.pkl'")

# Test prediction
test_input = "I feel very happy and joyful"
predicted_mood = pipeline.predict([test_input])[0]
print(f"\nTest input: {test_input}")
print(f"Predicted mood: {predicted_mood}")

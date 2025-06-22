import json
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

# Load the JSON
with open('intents.json') as file:
    data = json.load(file)

# Flatten JSON into DataFrame
records = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        records.append({
            "pattern": pattern,
            "tag": intent["tag"]
        })

df = pd.DataFrame(records)

# Features and labels
X = df['pattern']
y = df['tag']

# Vectorize
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Encode labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train model
model = LogisticRegression()
model.fit(X_vectorized, y_encoded)

# Save all components
with open('intents.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)

print("✅ Model trained and saved using pandas.")

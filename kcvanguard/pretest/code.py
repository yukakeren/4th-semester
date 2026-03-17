import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from catboost import CatBoostClassifier

# 1. Load Data
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# 2. Basic Cleaning
def clean_text(text):
    if pd.isna(text): return "unknown"
    # Remove brackets like [ 1 ] and convert to lowercase
    return str(text).lower().replace('[', '').replace(']', '').replace('1', '')

for df in [train, test]:
    df['genre'] = df['genre'].apply(clean_text)
    df['creator'] = df['creator'].apply(clean_text)
    df['title_clean'] = df['title'].apply(clean_text)

# 3. Feature Engineering: Target Encoding for Creators
# (Creators are highly predictive of the network)
# 4. Prepare Features
features = ['release_year', 'episode_count', 'num_seasons', 'duration_minutes', 
            'episode_format', 'animation_type', 'genre', 'creator', 'country']

# Handle categorical indices for CatBoost
cat_features = ['episode_format', 'animation_type', 'genre', 'creator', 'country']

# 5. Train Model
model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    loss_function='MultiClass',
    cat_features=cat_features,
    verbose=100
)

X = train[features].fillna(-1)
y = train['network']

model.fit(X, y)

# 6. Predict
test_X = test[features].fillna(-1)
predictions = model.predict(test_X)

# 7. Create Submission
submission = pd.DataFrame({'id': test['id'], 'network': predictions.flatten()})
submission.to_csv('submission.csv', index=False)
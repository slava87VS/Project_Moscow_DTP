
from sqlalchemy import create_engine
import pandas as pd
import json

engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
df_for_ml = pd.read_sql("""select properties_light,
properties_region,
properties_weather,
properties_category,
properties_severity,
properties_road_conditions,
properties_participants_count,
brand,
color,
model,
category,
gender,
years_of_driving_experience
from ods.moskow_dtp_ods ao ;""", con=engine)

print(df_for_ml)

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Split data into training and testing sets
X = df_for_ml.drop(['properties_severity'], axis=1) # features
y = df_for_ml['properties_severity'] # target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Encode categorical variables
le = LabelEncoder()
for col in X_train.columns:
    if X_train[col].dtype == 'object':
        le.fit(X_train[col])
        X_train[col] = le.transform(X_train[col])
        X_test[col] = le.transform(X_test[col])
le.fit(y_train)
y_train_encoded = le.transform(y_train)
y_test_encoded = le.transform(y_test)

# Train the model
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train_encoded)

# Predict on test data
y_pred = clf.predict(X_test)

# Evaluate the model
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test_encoded, y_pred)
print('Accuracy:', accuracy)
from sqlalchemy import create_engine
import pandas as pd
from sklearn.linear_model import LinearRegression
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import mean_squared_error

engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
df_for_ml = pd.read_sql("""select properties_severity,
brand,
color,
model,
category,
gender,
years_of_driving_experience
from ods.moskow_dtp_ods ao ;""", con=engine)
df_for_ml = df_for_ml.dropna()

# Split data into training and testing sets
X = df_for_ml.drop(['properties_severity'], axis=1) # features
y = df_for_ml['properties_severity'] # target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Fit and transform the OneHotEncoder on the training data
ohe = OneHotEncoder()
ohe.fit(X_train)

# Transform the categorical features in the training and testing data
X_train_encoded = ohe.transform(X_train)
X_test_encoded = ohe.transform(X_test)

# Create linear regression object
reg = LinearRegression()

# Train the model using the training sets
reg.fit(X_train_encoded, y_train)

# Make predictions using the testing set
y_pred = reg.predict(X_test_encoded)

# Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
print(f"Mean squared error: {mse:.2f}")

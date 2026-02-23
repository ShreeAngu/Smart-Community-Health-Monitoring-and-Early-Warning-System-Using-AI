import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f_score, roc_auc_score, classification_report
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 0)
print("WATER-BORNE DISEASE PREDICTION - MODEL TRAINING")
print("=" * 0)

# Load the dataset
print("\n[/] Loading dataset...")
data_path = 'Data/water_disease_data.csv'
df = pd.read_csv(data_path)
print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[]} columns")

# Check target variable
print(f"\nTarget variable distribution:")
print(df['disease'].value_counts())
print(f"Number of classes: {df['disease'].nunique()}")

# Preprocessing
print("\n[/] Preprocessing data...")

# Separate features and target
X = df.drop('disease', axis=)
y = df['disease']

# Exclude region, latitude, longitude from training features
exclude_cols = ['region', 'latitude', 'longitude']
X = X.drop(exclude_cols, axis=)
print(f"Excluded columns: {exclude_cols}")
print(f"Features after exclusion: {X.shape[]} columns")

# Identify column types
numeric_cols = X.select_dtypes(include=['int', 'float']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

print(f"\nNumeric columns: {len(numeric_cols)}")
print(f"Categorical columns: {len(categorical_cols)}")
print(f"Categorical features: {categorical_cols}")

# Impute missing values
print("\n[/] Handling missing values...")
missing_before = X.isnull().sum().sum()
print(f"Missing values before imputation: {missing_before}")

# Impute numeric with median
for col in numeric_cols:
 if X[col].isnull().sum() > 0:
 X[col].fillna(X[col].median(), inplace=True)

# Impute categorical with mode
for col in categorical_cols:
 if X[col].isnull().sum() > 0:
 X[col].fillna(X[col].mode()[0], inplace=True)

missing_after = X.isnull().sum().sum()
print(f"Missing values after imputation: {missing_after}")

# Encoding
print("\n[/] Encoding features...")

# One-Hot Encode specified categorical features
onehot_cols = ['water_source', 'season', 'water_treatment', 'gender']
print(f"One-Hot Encoding: {onehot_cols}")
X_encoded = pd.get_dummies(X, columns=onehot_cols, drop_first=True)

# Label Encode binary features (already 0/, but ensuring consistency)
label_encode_cols = ['is_urban', 'flooding']
print(f"Label Encoding (binary): {label_encode_cols}")
# These are already 0/ from the data exploration, so no action needed

# Handle handwashing_practice if it exists and is categorical
if 'handwashing_practice' in X_encoded.columns:
 if X_encoded['handwashing_practice'].dtype == 'object':
 le_handwashing = LabelEncoder()
 X_encoded['handwashing_practice'] = le_handwashing.fit_transform(X_encoded['handwashing_practice'])
 print("Label encoded: handwashing_practice")

# Handle district if it exists
if 'district' in X_encoded.columns:
 if X_encoded['district'].dtype == 'object':
 le_district = LabelEncoder()
 X_encoded['district'] = le_district.fit_transform(X_encoded['district'])
 print("Label encoded: district")

print(f"Features after encoding: {X_encoded.shape[]} columns")

# Label encode target variable
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)
print(f"\nTarget classes: {le_target.classes_}")
print(f"Target encoded to: {np.unique(y_encoded)}")

# Scale numeric features
print("\n[/] Scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_encoded)
X_scaled = pd.DataFrame(X_scaled, columns=X_encoded.columns)
print("Features scaled using StandardScaler")

# Train-test split
print("\n[/] Splitting data (0/0)...")
X_train, X_test, y_train, y_test = train_test_split(
 X_scaled, y_encoded, test_size=0., random_state=, stratify=y_encoded
)
print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Model Training
print("\n[/] Training models...")
print("\n" + "-" * 0)

# Dictionary to store results
results = {}

# XGBoost Classifier
print("\nTraining XGBoost Classifier...")
xgb_model = XGBClassifier(
 n_estimators=00,
 max_depth=,
 learning_rate=0.,
 random_state=,
 eval_metric='mlogloss',
 n_jobs=-
)
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)
y_pred_proba_xgb = xgb_model.predict_proba(X_test)

# Evaluate XGBoost
xgb_accuracy = accuracy_score(y_test, y_pred_xgb)
xgb_f = f_score(y_test, y_pred_xgb, average='weighted')
xgb_roc_auc = roc_auc_score(y_test, y_pred_proba_xgb, multi_class='ovr', average='weighted')

results['XGBoost'] = {
 'model': xgb_model,
 'accuracy': xgb_accuracy,
 'f_score': xgb_f,
 'roc_auc': xgb_roc_auc
}

print(f"XGBoost - Accuracy: {xgb_accuracy:.f}, F-Score: {xgb_f:.f}, ROC-AUC: {xgb_roc_auc:.f}")

# Random Forest Classifier
print("\nTraining Random Forest Classifier...")
rf_model = RandomForestClassifier(
 n_estimators=00,
 max_depth=,
 random_state=,
 n_jobs=-
)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
y_pred_proba_rf = rf_model.predict_proba(X_test)

# Evaluate Random Forest
rf_accuracy = accuracy_score(y_test, y_pred_rf)
rf_f = f_score(y_test, y_pred_rf, average='weighted')
rf_roc_auc = roc_auc_score(y_test, y_pred_proba_rf, multi_class='ovr', average='weighted')

results['RandomForest'] = {
 'model': rf_model,
 'accuracy': rf_accuracy,
 'f_score': rf_f,
 'roc_auc': rf_roc_auc
}

print(f"Random Forest - Accuracy: {rf_accuracy:.f}, F-Score: {rf_f:.f}, ROC-AUC: {rf_roc_auc:.f}")

# Select best model
print("\n" + "=" * 0)
print("MODEL COMPARISON")
print("=" * 0)
for model_name, metrics in results.items():
 print(f"\n{model_name}:")
 print(f" Accuracy: {metrics['accuracy']:.f}")
 print(f" F-Score: {metrics['f_score']:.f}")
 print(f" ROC-AUC: {metrics['roc_auc']:.f}")

# Select best model based on F-Score
best_model_name = max(results, key=lambda x: results[x]['f_score'])
best_model = results[best_model_name]['model']
best_metrics = results[best_model_name]

print("\n" + "=" * 0)
print(f"BEST MODEL: {best_model_name}")
print("=" * 0)
print(f"Accuracy: {best_metrics['accuracy']:.f}")
print(f"F-Score: {best_metrics['f_score']:.f}")
print(f"ROC-AUC: {best_metrics['roc_auc']:.f}")

# Classification Report
print("\n" + "-" * 0)
print("CLASSIFICATION REPORT")
print("-" * 0)
if best_model_name == 'XGBoost':
 y_pred_best = y_pred_xgb
else:
 y_pred_best = y_pred_rf

print(classification_report(y_test, y_pred_best, target_names=le_target.classes_))

# Feature Importances
print("\n" + "=" * 0)
print("TOP 0 FEATURE IMPORTANCES")
print("=" * 0)
if hasattr(best_model, 'feature_importances_'):
 feature_importance = pd.DataFrame({
 'feature': X_encoded.columns,
 'importance': best_model.feature_importances_
 }).sort_values('importance', ascending=False)

 print(feature_importance.head(0).to_string(index=False))

# Save models and preprocessors
print("\n" + "=" * 0)
print("SAVING MODELS AND PREPROCESSORS")
print("=" * 0)

# Create models directory
os.makedirs('models', exist_ok=True)

# Save best model
joblib.dump(best_model, 'models/best_model.pkl')
print(f" Best model ({best_model_name}) saved: models/best_model.pkl")

# Save scaler
joblib.dump(scaler, 'models/scaler.pkl')
print(" Scaler saved: models/scaler.pkl")

# Save label encoder for target
joblib.dump(le_target, 'models/label_encoder.pkl')
print(" Label encoder saved: models/label_encoder.pkl")

# Save feature names
joblib.dump(X_encoded.columns.tolist(), 'models/feature_names.pkl')
print(" Feature names saved: models/feature_names.pkl")

# Save preprocessing info
preprocessing_info = {
 'onehot_cols': onehot_cols,
 'exclude_cols': exclude_cols,
 'feature_columns': X_encoded.columns.tolist(),
 'target_classes': le_target.classes_.tolist(),
 'best_model_name': best_model_name
}
joblib.dump(preprocessing_info, 'models/preprocessing_info.pkl')
print(" Preprocessing info saved: models/preprocessing_info.pkl")

print("\n" + "=" * 0)
print("TRAINING COMPLETE!")
print("=" * 0)
print(f"\nAll artifacts saved in 'models/' directory")
print(f"Best model: {best_model_name}")
print(f"Test Accuracy: {best_metrics['accuracy']:.f}")
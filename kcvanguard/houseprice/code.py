import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool

train = pd.read_csv('/kaggle/input/competitions/house-prices-advanced-regression-techniques/train.csv')
test = pd.read_csv('/kaggle/input/competitions/house-prices-advanced-regression-techniques/test.csv')

# --- Feature engineering ---
for df in [train, test]:
    df['TotalSF'] = df['TotalBsmtSF'].fillna(0) + df['1stFlrSF'] + df['2ndFlrSF']
    df['TotalBath'] = (df['FullBath'] + 0.5 * df['HalfBath']
                       + df['BsmtFullBath'].fillna(0) + 0.5 * df['BsmtHalfBath'].fillna(0))
    df['TotalPorchSF'] = (df['OpenPorchSF'] + df['EnclosedPorch']
                          + df['3SsnPorch'] + df['ScreenPorch'] + df['WoodDeckSF'])
    df['HasGarage'] = df['GarageArea'].apply(lambda x: 1 if x > 0 else 0)
    df['HouseAge'] = df['YrSold'] - df['YearBuilt']
    df['RemodAge'] = df['YrSold'] - df['YearRemodAdd']

# Strong numeric + categorical features
features = [
    # Numeric – size & quality
    'OverallQual', 'OverallCond', 'GrLivArea', 'TotalSF',
    'TotalBsmtSF', '1stFlrSF', '2ndFlrSF',
    'GarageArea', 'GarageCars',
    'TotalBath', 'TotalPorchSF',
    'LotArea', 'LotFrontage', 'MasVnrArea',
    'BsmtFinSF1', 'BsmtUnfSF',
    'Fireplaces', 'WoodDeckSF',
    # Numeric – age / time
    'YearBuilt', 'YearRemodAdd', 'HouseAge', 'RemodAge',
    'GarageYrBlt', 'MoSold', 'YrSold',
    # Categorical
    'MSSubClass', 'MSZoning', 'Neighborhood',
    'Condition1', 'BldgType', 'HouseStyle',
    'RoofStyle', 'Exterior1st', 'Exterior2nd',
    'ExterQual', 'ExterCond',
    'Foundation', 'BsmtQual', 'BsmtExposure', 'BsmtFinType1',
    'HeatingQC', 'CentralAir', 'Electrical',
    'KitchenQual', 'Functional',
    'FireplaceQu', 'GarageType', 'GarageFinish',
    'GarageQual', 'PavedDrive',
    'SaleType', 'SaleCondition',
    'LotShape', 'LandContour', 'LotConfig',
    'HasGarage',
]

# Categorical columns (explicitly listed to work across pandas versions)
cat_features = [
    'MSSubClass', 'MSZoning', 'Neighborhood',
    'Condition1', 'BldgType', 'HouseStyle',
    'RoofStyle', 'Exterior1st', 'Exterior2nd',
    'ExterQual', 'ExterCond',
    'Foundation', 'BsmtQual', 'BsmtExposure', 'BsmtFinType1',
    'HeatingQC', 'CentralAir', 'Electrical',
    'KitchenQual', 'Functional',
    'FireplaceQu', 'GarageType', 'GarageFinish',
    'GarageQual', 'PavedDrive',
    'SaleType', 'SaleCondition',
    'LotShape', 'LandContour', 'LotConfig',
]

# Prepare data
X_train = train[features].copy()
y_train = np.log1p(train['SalePrice'])  # log-transform target for better RMSE
X_test = test[features].copy()

# Fill NaN in categorical columns with "Missing" so CatBoost handles them
for c in cat_features:
    X_train[c] = X_train[c].fillna('Missing').astype(str)
    X_test[c] = X_test[c].fillna('Missing').astype(str)

# MSSubClass is numeric but categorical — convert to string
X_train['MSSubClass'] = X_train['MSSubClass'].astype(str)
X_test['MSSubClass'] = X_test['MSSubClass'].astype(str)

model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.1,
    depth=6,
    l2_leaf_reg=3,
    loss_function='RMSE',
    random_seed=101,
    task_type='CPU',
    bootstrap_type='MVS',
    verbose=200,
)

train_pool = Pool(X_train, y_train, cat_features=cat_features)

model.fit(train_pool)

test_pool = Pool(X_test, cat_features=cat_features)
predictions = np.expm1(model.predict(test_pool))  # reverse log-transform

submission = pd.DataFrame({'Id': test['Id'], 'SalePrice': predictions})
submission.to_csv('submission.csv', index=False)
print(f'Submission saved – {len(submission)} rows')

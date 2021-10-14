import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

def clean_missing_ts(one, two):
    if one.shape[0] > two.shape[0]:
        for row1 in one.index:
            if not row1 in two.index:
                one = one.drop(row1)
    else:
         for row1 in two.index:
            if not row1 in one.index:
                two = two.drop(row1)
    return one, two


raw_data = pd.read_parquet('./hectare_data/heatlive_allaitant_prod_ia/ax_raw/FR4920153124_2018-11-17.parquet')
raw_data.index = pd.to_datetime(raw_data.index).floor("5T")
normalized_data = pd.read_parquet('./hectare_data/heatlive_allaitant_prod_ia/normalized/FR4920153124_2018-11-17.parquet')

raw_data = raw_data.sort_index()
normalized_data = normalized_data.sort_index()
print(normalized_data)

# print('normalized_data = ', normalized_data)

data_train = raw_data.loc['2018-10-23':'2018-10-26']
updata_train = normalized_data.loc['2018-10-23':'2018-10-26']

updata_train = updata_train['Up']


print(data_train.info())
print(data_train.isna().sum())
data_train, updata_train = clean_missing_ts(data_train, updata_train)

updata_train = np.array(updata_train.astype('int'))
vars = np.array(data_train[['EAn','EAg','Egx','ChAn','ChAg','Chgx','EtAg','Etgx','P0An']])
# vars = np.array(data_train[['ChAn', 'Chgx']])

logisticRegr = LogisticRegression(solver='saga', max_iter=10000).fit(vars, updata_train)
# logisticRegr.predict_proba(vars)
Y_hat = logisticRegr.predict(vars)

print("score : ", logisticRegr.score(vars, updata_train))
print("intercept : ", logisticRegr.intercept_)
print("coef : ", logisticRegr.coef_)

plt.scatter(data_train.index, updata_train)
plt.scatter(data_train.index, Y_hat + 0.2)
# plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

def add_intercept(x):
    return (np.c_[np.ones((x.shape[0],1)), x])

def predict(x, theta):
    X = add_intercept(x)
    return 1 / (1 + np.exp(-X @ theta))

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


raw_data = pd.read_parquet('./hectare_data/heatlive_allaitant_prod_ia/ax_raw/FR4973400352_2018-11-03.parquet')
raw_data.index = pd.to_datetime(raw_data.index).floor("5T")
normalized_data = pd.read_parquet('./hectare_data/heatlive_allaitant_prod_ia/normalized/FR4973400352_2018-11-03.parquet')

raw_data = raw_data.sort_index()
normalized_data = normalized_data.sort_index()
print(normalized_data)

# print('normalized_data = ', normalized_data)

first_day = normalized_data.index[0]
day_after = first_day + pd.DateOffset(4)
print(first_day, day_after)

data_train = raw_data.loc[first_day:day_after]
updata_train = normalized_data.loc[first_day:day_after]

updata_train = updata_train['Up']

# print(data_train.info())
# print(data_train.isna().sum())
data_train, updata_train = clean_missing_ts(data_train, updata_train)

updata_train = np.array(updata_train.astype('int'))
# print(data_train[['EAn','EAg','Egx','ChAn','ChAg','Chgx','EtAg','Etgx','P0An']])
vars = np.array(data_train[['EAn','EAg','Egx','ChAn','ChAg','Chgx','EtAg','Etgx','P0An']])

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
print(data_train)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(vars, updata_train, test_size=0.4)

logisticRegr = KNeighborsClassifier().fit(X_train, y_train)
# logisticRegr.predict_proba(vars)
Y_hat = logisticRegr.predict(X_test)

print("score : ", logisticRegr.score(X_test, y_test))
# print("intercept : ", logisticRegr.intercept_)
# print("coef : ", logisticRegr.coef_)

plt.scatter(data_train.index, updata_train, marker=2)
plt.scatter(data_train.index, Y_hat + 0.2, marker=2)
plt.show()
exit(0)

Y_hat  = logisticRegr.predict(vars)
Y_hat_raw  = logisticRegr.predict(vars)
line  = logisticRegr.predict(vars)

for i, elem in enumerate(Y_hat):
    line[i] = 0.5
    if elem > 0.5:
        Y_hat[i] = 1
    else:
        Y_hat[i] = 0

# print('log_loss(updata_train, Y_hat) = ', log_loss(updata_train, Y_hat))

print("Accuracy: " + str(logisticRegr.score(vars, Y_hat) * 100) + "%")
plt.title("Accuracy: " + str(logisticRegr.score(vars, Y_hat) * 100) + "%")
plt.scatter(data_train.index, Y_hat_raw, marker=2, label="raw ŷ")
plt.scatter(data_train.index, Y_hat + 0.05, marker=2, label="ŷ")
plt.scatter(data_train.index, updata_train + 0.1, marker=2, label="normalized")
plt.plot(data_train.index, line)
# plt.plot([1,2], [0.5, 0.5])
# plt.plot([1,2], np.full(range(len(data_train)), 0.5))
plt.legend()
plt.show()


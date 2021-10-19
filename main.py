import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import STL
import statsmodels.api as sm
# import statsmodels.api as sm
# import seaborn; seaborn.set()

plt.rcParams["figure.figsize"] = (20,9)

# raw = ['EAg', 'EAn', 'Egx', 'Chgx', 'ChAg', 'ChAn', 'EtAG', 'EtGx', 'P0An']
# normalized = ['Rumination', 'Ingestion', 'OverActivity', 'Other Activity', 'Rest']
root = 'hectare_data/heatlive_allaitant_ms/'
metadata_csv = root + 'metadata.csv'
normalized = root + 'normalized/'
ax = root + 'ax_raw/'

state_compare = ['Rumination', 'Ingestion_at_trough',
                 'Ingestion_at_pasture', 'OverActivity', 'Rest']
# state_compare = ['Up']
# state_compare = ['Rumination']

def set_state(df):
    for index, state in df[state_compare].iteritems():
        if state == True:
            df['State'] = index
    return df

def rename_raw_data(raw_data):
    return raw_data.rename(columns={ \
                'EAn': "moyenne de l'acceleration en n", \
                'EAg': "moyenne de l'acceleration en g", \
                'Egx': "moyenne de l'acceleration en x", \

                'ChAn': 'somme acceleration (absolue) en n', \
                'ChAg': 'somme acceleration (absolue) en g', \
                'Chgx': 'somme acceleration (absolue) en x', \

                'P0An': 'nombre de passages par 0 de l’accélération sur axe N sur les 5 min', \
                'EtAg': 'écart-type de l’accélération sur axe g sur les 5 min', \
                'Etgx': ' écart-type de l’accélération sur axe x sur les 5 min', \
            })

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(2)

def predict(state_dic, raw_events, normalized_events):
    state_dic = state_dic.apply(set_state, axis=1).dropna()
    raw_events = state_dic[raw_events.columns]

    X_train, X_test, y_train, y_test = train_test_split(raw_events, state_dic['State'], test_size=0.4)
    X_train = poly.fit_transform(X_train)

    lr = LogisticRegression(solver='sag', C=100000.0, max_iter=10000000).fit(X_train, y_train)
    score =  round(lr.score(poly.transform(X_test), y_test) * 100, 1)
    print("score: ", score)
    # print("score : ", lr.score(X_test, y_test))

def state_pair_plot(normalized_events, raw_events):
    state_dic = pd.concat([normalized_events, raw_events], axis=1)

    state_dic = state_dic.apply(set_state, axis=1)
    state_dic = state_dic.drop(columns=['Rumination', 'Ingestion_at_trough',
                                        'Ingestion_at_pasture', 'OverActivity',
                                        'Rest', 'Up', 'OtherActivity'])
    state_dic = state_dic.interpolate().dropna()
    sns.pairplot(state_dic, hue='State',
                 corner=True,
                 diag_kws=dict(fill=False),)
    # g.map_lower(sns.kdeplot, levels=4, color=".2")
    plt.show()


def plot_all(raw_events, normalized_events):
        normalized_events_len = normalized_events.shape[1]
        # fig, axes = plt.subplots(normalized_events_len + raw_events.shape[1], 1, sharex=True)
        # normalized_events.plot(ax=axes[:normalized_events_len], subplots=True)
        # raw_events.plot(ax=axes[normalized_events_len:], subplots=True)

        # raw_events.hist()
        # normalized_events.hist()

        ### Plot date###
        # plt.plot_date(normalized_events.index,
        #               raw_events['EAn'].astype('int'), 
        #               linestyle='--')

        ## seasonal decomposition
        sm.tsa.seasonal_decompose(raw_events['EAn'], period=12*6).plot()

        ## LAG PLOT ##
        # pd.plotting.lag_plot(raw_events['ChAg'], lag=1)

        ## Auto Correlation plot ##
        ## TODO : resample, since autocorrelation is used to find repeating 
        #         cycle, its better to use day/week/season
        # pd.plotting.autocorrelation_plot(raw_events['ChAg'])

        plt.show()


def reduce_to_one_day(normalized_events, raw_events):
    first_day = normalized_events.index[0]
    day_after = first_day + pd.DateOffset(1)

    normalized_events = normalized_events.loc[first_day : day_after]
    raw_events = raw_events.loc[first_day: day_after]
    return normalized_events, raw_events

def plot_one(raw_events, normalized_events):
    if (normalized_events.shape[0] < 1):
        return

    #TODO: move this after reducing to one day (fix the na problem) 
    state_dic = pd.concat([normalized_events, raw_events], axis=1)
    normalized_events = state_dic[normalized_events.columns]
    raw_events = state_dic[raw_events.columns]

    normalized_events, raw_events = reduce_to_one_day(normalized_events, raw_events)

    # raw_events = rename_raw_data(raw_events)
    plot_all(raw_events, normalized_events)
    # state_pair_plot(normalized_events, raw_events)

def floor_event(event): return event.index.floor('5T').floor('Min')

class Csv_reader():
    def get_data(self):
        return [self.raw_events, self.normalized_events]

    def __init__(self, csv_name):
        self.set_data(csv_name)

    def floor_events(self):
        self.normalized_events.index = floor_event(self.normalized_events)
        self.raw_events.index = floor_event(self.raw_events)

    def set_data(self, csv_name):
        csv = pd.read_csv(csv_name)
        row = csv.iloc[1].sort_index()
        event = row['event_id'] 
        self.normalized_events = pd.read_parquet(normalized + event + '.parquet').fillna(False)
        self.raw_events = pd.read_parquet(ax + event + '.parquet').interpolate()
        self.floor_events()

def save_df(df, fileName="text.txt"):
    tfile = open(fileName, 'w+')
    tfile.write(df.to_string())
    tfile.close()

def main():
    csv = Csv_reader(metadata_csv)
    plot_one(csv.raw_events, csv.normalized_events)
    merge = pd.merge_asof(csv.raw_events, csv.normalized_events,
                        left_index=True, right_index = True, tolerance=pd.Timedelta("5T"))
    concat = pd.concat([csv.normalized_events, csv.raw_events], axis=1)
    merge = merge.dropna()
    predict(merge, csv.raw_events, csv.normalized_events)
    # print(merge)

    # for index, row in csv.sort_index().iterrows():
    #     plot_one(row)

if __name__ == '__main__':
    main()


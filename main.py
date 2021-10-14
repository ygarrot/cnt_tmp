import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import seaborn; seaborn.set()

# raw = ['EAg', 'EAn', 'Egx', 'Chgx', 'ChAg', 'ChAn', 'EtAG', 'EtGx', 'P0An']
# normalized = ['Rumination', 'Ingestion', 'OverActivity', 'Other Activity', 'Rest']
root = 'hectare_data/heatlive_allaitant_ms/'
metadata_csv = root + 'metadata.csv'
normalized = root + 'normalized/'
ax = root + 'ax_raw/'

state_compare = ['Rumination', 'Ingestion_at_trough', 'Ingestion_at_pasture', 'OverActivity', 'Rest']
# state_compare = ['Up']

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

def state_pair_plot(normalized_events, raw_events):
    state_dic = pd.concat([normalized_events, raw_events], axis=1)
    # pd.plotting.autocorrelation_plot(normalized_events['Rumination'])
    state_dic = state_dic.apply(set_state, axis=1)
    state_dic = state_dic.drop(columns=['Rumination', 'Ingestion_at_trough',
                                        'Ingestion_at_pasture', 'OverActivity',
                                        'Rest', 'Up', 'OtherActivity'])
    state_dic = state_dic.interpolate().dropna()
    sns.pairplot(state_dic, hue='State')
    plt.show()


def plot_all(normalized_events, raw_events):
        print(normalized_events.shape)
        normalized_events_len = normalized_events.shape[1]
        # fig, axes = plt.subplots(normalized_events_len + raw_events.shape[1], 1, sharex=True)
        # normalized_events.plot(ax=axes[:normalized_events_len], subplots=True)
        # raw_events.plot(ax=axes[normalized_events_len:], subplots=True)

        # raw_events.hist()
        # normalized_events.hist()
        # sns.pairplot(raw_events, hue='State')
        print(normalized_events['Rumination'])

        plt.plot_date(normalized_events.index,
                      normalized_events['Rumination'].astype('int'), 
                      linestyle='--')

        ## LAG PLOT ##
        # pd.plotting.lag_plot(raw_events['ChAg'], lag=1)

        plt.show()

def floor_events(*events):
        for event in events:
            event.index = event.index.floor('5T').floor('Min') 
        return events

#     dic = {}
#     for index, row in csv.sort_index().iterrows():
def plot_one(row):
    event = row['event_id'] 
    normalized_events = pd.read_parquet(normalized + event + '.parquet').fillna(False)
    # raw_events = pd.read_parquet(ax + event + '.parquet')[['EAn', 'EAg', 'Egx']].interpolate()
    raw_events = pd.read_parquet(ax + event + '.parquet').interpolate()
    if (normalized_events.shape[0] < 1):
        return
    print(normalized_events.index[0])
    normalized_events = normalized_events.loc['2019-02-06':'2019-02-07']
    raw_events = raw_events.loc['2019-02-06':'2019-02-07']
    # raw_events = rename_raw_data(raw_events)
    raw_events, normalized_events = floor_events(raw_events, normalized_events)

    # plot_all(normalized_events, raw_events)
    # state_pair_plot(normalized_events, raw_events)

def main():
    csv = pd.read_csv(metadata_csv)
    # plot_one(csv.iloc[0].sort_index())
    for index, row in csv.sort_index().iterrows():
        plot_one(row)

if __name__ == '__main__':
    main()


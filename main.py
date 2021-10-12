import pandas as pd
import matplotlib.pyplot as plt

root = 'hectare_data/heatlive_allaitant_ms/'
metadata_csv = root + 'metadata.csv'
normalized = root + 'normalized/'
ax = root + 'ax_raw/'

def main():
    csv = pd.read_csv(metadata_csv)
    dic = {}

    for index, row in csv.sort_index().iterrows():
        event = row['event_id'] 
        normalized_event = pd.read_parquet(normalized + event + '.parquet').fillna(False)
        raw_event = pd.read_parquet(ax + event + '.parquet')[['EAn', 'EAg', 'Egx']].interpolate()
        # raw_event = pd.read_parquet(ax + event + '.parquet').interpolate()
        raw_event = raw_event.rename(columns={ \
                'EAn': "moyenne de l'acceleration en n", \
                'EAg': "moyenne de l'acceleration en g", \
                'Egx': "moyenne de l'acceleration en x", \
                'ChAn': 'somme acceleration (absolue) en n', \
                'ChAg': 'somme acceleration (absolue) en g', \
                'ChAgx': 'somme acceleration (absolue) en x', \
            })
        normalized_event.index = normalized_event.index.floor('5T')
        normalized_event.index = normalized_event.index.floor('Min')

        raw_event.index = raw_event.index.floor('5T')
        raw_event.index = raw_event.index.floor('Min')


        raw_event_len = 3 # len(raw_event)
        normalized_event_len = 7 #len(normalized_event)

        fig, axes = plt.subplots(normalized_event_len + raw_event_len, 1, sharex=True)
        normalized_event.plot(ax=axes[:normalized_event_len], subplots=True)
        raw_event.plot(ax=axes[normalized_event_len:],subplots=True)
        plt.show()
        # dic.setdefault(row['cow_id'], []).append(pd.concat([normalized_event, raw_event], axis=1))

    for idx, cow in dic.items():
        # print(cow[0])
        # print(cow[0].fillna(False))
        cow[0].fillna(False).plot(subplots=True)
        plt.show()
        # exit(0)
    print(dic)

if __name__ == '__main__':
    main()

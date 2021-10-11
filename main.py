import pandas as pd
import pandas as pd

root = 'hectare_data/heatlive_allaitant_ms/'
metadata_csv = root + 'metadata.csv'
normalized = root + 'normalized/'
ax = root + 'ax_raw/'

def main():
    csv = pd.read_csv(metadata_csv)
    dic = {}

    for index, row in csv.sort_index().iterrows():
        event = row['event_id'] 
        event_normalized = pd.read_parquet(normalized + event + '.parquet')
        event_ax = pd.read_parquet(ax + event + '.parquet')
        dic.setdefault(row['cow_id'], []).append(pd.concat([event_normalized, event_ax]))
        # print(dic[row['cow_id']].index())
    print(dic)

if __name__ == '__main__':
    main()

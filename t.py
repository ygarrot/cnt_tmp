import pandas as pd
import numpy as np

def print_dataframe_to_file(df, fileName="text.txt"):
    tfile = open(fileName, 'w+')
    tfile.write(df.to_string())
    tfile.close()

# only add the link to the raw, it will replace it with normalize to get both files
links_to_raw = [
                # './hectare_data/heatlive_allaitant_prod_ia/ax_raw/FR0200546256_2016-12-28.parquet',
                './hectare_data/heatlive_allaitant_prod_ia/ax_raw/FR0200546527_2016-12-20.parquet',
            ]

# tmp_raw = []
# tmp_normalized = []
data = []
for link in links_to_raw:
    raw_file = pd.read_parquet(link)
    normalized_file = pd.read_parquet(link.replace('ax_raw', 'normalized'))
    data.append(pd.concat([raw_file, normalized_file], axis=1))
    print(data)
            
    # tmp_raw.append(pd.read_parquet(links_to_raw[i]))
    # tmp_normalized.append(normalized_file)

print(pd.concat(data))
# raw = pd.concat(tmp_raw)
# normalized = pd.concat(tmp_normalized)

# round to 5 min, important for indexes to match
raw.index = pd.to_datetime(raw.index).floor("5T")
normalized.index = pd.to_datetime(normalized.index).floor("5T")

raw = raw.sort_index()
normalized = normalized.sort_index()

data = pd.merge(raw, normalized, left_index=True, right_index=True)

# data = data.dropna()
data = data[~data.index.duplicated(keep='first')]
print_dataframe_to_file(data)

print('raw.shape = ', raw.shape)
print('normalized.shape = ', normalized.shape)
print('data.shape = ', data.shape)
# Output:
# raw.shape =  (19963, 9)
# normalized.shape =  (17358, 7)
# data.shape =  (28327, 16)


def main():
    csv = pd.read_csv(metadata_csv)
    plot_one(csv.iloc[0].sort_index())
    # for index, row in csv.sort_index().iterrows():
    #     plot_one(row)

if __name__ == '__main__':
    main()


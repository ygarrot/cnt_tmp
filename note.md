# GOAL:
vêlage est imminent ou si l’animal présente un comportement de chaleurs

# TODO lundi:

organiser les données
Tracer les saisons, resample, confusion matrix
Essayer de faire une regression logistic avec les 5 colonnes a predire
('Rumination', 'Ingestion', 'OverActivity', 'Other Activity', 'Rest'])
Il faut au moins les données d'une vache sur une année



outliers: valeurs aberrantes
scatter plot= nuage de point
gamut=gamme

## www.itl.nist.gov
role of graphics: https://www.itl.nist.gov/div898/handbook/eda/section1/eda15.htm

General problem Categories: https://www.itl.nist.gov/div898/handbook/eda/section1/eda17.htm
(conseil pour le choix des graphes)

Inasmuch = Dans la mesure

lag plot = scatter plot + lag (y + n) typiquement n + 1

## seasonal decomposition statsmodels
sm.tsa.seasonal_decompose(df[], period=12*6).plot()

## matrix comparison
```python
print(data_train.info())
print(data_train.isna().sum())
```

## Ajouter un offset a un timestamp
```python
pd.DatetimeIndex(df.date) + pd.DateOffset(1)
d.DatetimeIndex(df.date) + pd.offsets.Hour(1)
```

## merge with timestamp index
```python
state_dic = pd.merge(normalized_events, raw_events, how='outer', left_index=True, right_index=True)
state_dic = pd.concat([normalized_events, raw_events], axis=1)
```

'foreach like' `state_dic.apply(set_state, axis=1)`

## Resume 
https://jakevdp.github.io/PythonDataScienceHandbook/03.11-working-with-time-series.html

resample() // asfreq()
The primary difference between the two is that resample() is fundamentally a data aggregation,
while asfreq() is fundamentally a data selection.

Rolling calculations take the size of the window as the argument, whereas resampling takes a frequency specifier as the argument.

shift() = decale seulement les data
and tshift() = decale le temps (index)

```
A common context for this type of shift is in computing differences over time. For example, we use shifted values to compute the one-year return on investment for Google stock over the course of the dataset:
```

## Decompose time series data trend seasonality
https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/




## Article specifique au time series
https://otexts.com/fpp2/intro.html
The “frequency” is the number of observations before the seasonal pattern repeats.

2.3 Time series patterns
In describing these time series, we have used words such as “trend” and “seasonal” which need to be defined more carefully.

Trend
A trend exists when there is a long-term increase or decrease in the data. It does not have to be linear. Sometimes we will refer to a trend as “changing direction,” when it might go from an increasing trend to a decreasing trend.

Seasonal
A seasonal pattern occurs when a time series is affected by seasonal factors such as the time of the year or the day of the week. Seasonality is always of a fixed and known frequency.

Cyclic
A cycle occurs when the data exhibit rises and falls that are not of a fixed frequency. These fluctuations are usually due to economic conditions, and are often related to the “business cycle.” The duration of these fluctuations is usually at least 2 years.

### Seasonal plots
A seasonal plot is similar to a time plot except that the data are plotted against the individual “seasons” in which the data were observed

##
http://earthpy.org/pandas-basics.html
rolling mean:
aonao.rolling(window=12, center=False).mean().plot(style='-g')

rolling correlation
aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g')

correlation:
aonao.corr()


## other
df.head

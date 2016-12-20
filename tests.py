import pandas as pd


df = pd.read_csv('./Armani.csv')

print(df.groupby('region').size())
print(
    df[((df['currency'] == 'EUR') & (df['region'] == 'FRANCE')) |
       ((df['currency'] == 'USD') & (df['region'] == 'UNITED STATES'))]
)

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', 500)
https://code-with-me.jetbrains.com/Gn9EGXiSPOODZXBancEy7g#p=PC&fp=653F6BA5CED2A3FB54E2C001387882DC6E1DFA1C1A76969AFB9EC3DFBA8F2BE3

file = '/home/user/Downloads/Timeseries_41.632_-0.905_SA_6kWp_crystSi_20_45deg_0deg_2005_2016.csv'

df = pd.DataFrame(pd.read_csv(file, skiprows=10,skipfooter=10))
print(df)
format1 ="%Y%m%d:%H%M"
format2 = "%Y-%m-%d %H:%M:%S"
df["time"] = df["time"].apply(lambda x: datetime.fromtimestamp(datetime.strptime(x, format1).timestamp()))
df.set_index(df['time'],drop=False,inplace=True)

df = df.drop('time',axis=1)

test = df.groupby([df.index.month, df.index.day,df.index.hour]).mean()
test= test.drop((2,29))


test.index = pd.to_datetime(test.index.get_level_values(0).astype(str) + '-' +
               test.index.get_level_values(1).astype(str)+ '-' +
               test.index.get_level_values(2).astype(str),
               format='%m-%d-%H')


dfh = pd.read_pickle('dfh.pkl')
dfh = dfh.replace('?', np.NaN)
dfh['wh'] = dfh['Global_active_power'].astype('float')*1000
dfh = dfh[['Date_Time','wh']]
dfh = dfh.groupby(pd.Grouper(key='Date_Time',freq='1h')).mean()

dfh = dfh.groupby([dfh.index.month, dfh.index.day,dfh.index.hour]).mean()
dfh= dfh.drop((2,29))
dfh.index = pd.to_datetime(dfh.index.get_level_values(0).astype(str) + '-' +
               dfh.index.get_level_values(1).astype(str)+ '-' +
               dfh.index.get_level_values(2).astype(str),
               format='%m-%d-%H')

dfh['wh'] = dfh['wh']*(3000000/dfh['wh'].sum())


precio = pd.DataFrame(pd.read_excel('/home/user/Downloads/71-PVPC_DETALLE_DD-2021-08-11T23 59 59+00 00.xls',skiprows=4,skipfooter=1))
precio['precio'] = precio["Término energía PVPC\nFEU = TEU + TCU\n€/MWh consumo"]/1000
test['precio'] = np.tile(precio['precio'],365)
test['diferencia'] = test['G(i)']*37.993536-dfh['wh']-1000
test['a pagar'] = -test[test['diferencia']<0]['diferencia']/1000 * test[test['diferencia']<0]['precio']
test['a pagar'] = test['a pagar'].fillna(0)
print(test['a pagar'].sum())
print(test[test['diferencia']<0]['precio'].mean())
fig, (ax,ax1) = plt.subplots(1,2)
ax.plot(test['diferencia'],label = 'Diferencia ')
ax1.plot(test['a pagar'])
plt.show()
plt.plot(test['G(i)']*38)
plt.plot(test['diferencia'])
plt.show()
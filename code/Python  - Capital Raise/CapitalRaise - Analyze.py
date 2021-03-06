# %%
import os
import pandas as pd
import numpy as np
import re
import statsmodels.api as sm
import finance_byu.rolling as rolling


def convert_ar_characters(input_str):

    mapping = {
        "ك": "ک",
        "گ": "گ",
        "دِ": "د",
        "بِ": "ب",
        "زِ": "ز",
        "ذِ": "ذ",
        "شِ": "ش",
        "سِ": "س",
        "ى": "ی",
        "ي": "ی",
    }
    return _multiple_replace(mapping, input_str)


def _multiple_replace(mapping, text):
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))


def vv(row):
    X = row.split("-")
    return int(X[0] + X[1] + X[2])


def vv2(row):
    X = row.split("/")
    return int(X[0] + X[1] + X[2])


path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"


# %%
df2 = pd.read_csv(path + "adjPrices_1399-11-06.csv")
df2.Date = df2.Date.apply(vv)
df2 = df2.drop(columns="Unnamed: 0").rename(columns={"ID": "stock_id", "Date": "date"})


# %%
df = pd.read_excel(path + "Capital Rise - 71-99.xlsx")
df = df[df.CapAfter != df.CapBefore]
df = df[~df.Symbol.isnull()].rename(columns={"Symbol": "name"})
df = df[
    [
        "name",
        "year",
        "Firm",
        "CapAfter",
        "CapBefore",
        "ExtOrdGMDate",
        "Revaluation",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "JustRevaluation",
        "Hybrid",
        "%CapRaised",
        "%PremiumCapRaising",
        "%ROCapRaising",
        "%SavingCapRaising",
    ]
]


df["CapBefore2"] = (df["CapBefore"] / 10).round(0)
df["CapAfter2"] = (df["CapAfter"] / 10).round(0)
df["ExtOrdGMDate2"] = (df["ExtOrdGMDate"] / 10).round(0)

df = df.drop_duplicates(subset=["name", "CapAfter2", "CapBefore2"], keep="first")
df = df.drop_duplicates(subset=["ExtOrdGMDate2", "CapBefore2"], keep="first")
df = df.drop_duplicates(subset=["ExtOrdGMDate2", "CapAfter2"], keep="first")
df = df.drop_duplicates(subset=["ExtOrdGMDate", "CapBefore2"], keep="first")
df = df.drop_duplicates(subset=["ExtOrdGMDate", "CapAfter2"], keep="first")

df = df[df.CapBefore != 0]
df["Percent"] = ((df["CapAfter"] - df["CapBefore"]) / df["CapBefore"]) * 100
df["Percent"] = df["Percent"].round(2)
df = df[df.Percent > 0]

df = df[
    [
        "name",
        "year",
        "Firm",
        "CapAfter",
        "CapBefore",
        "ExtOrdGMDate",
        "Revaluation",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "JustRevaluation",
        "Hybrid",
        "%CapRaised",
        "%PremiumCapRaising",
        "%ROCapRaising",
        "%SavingCapRaising",
    ]
]
df = df.drop_duplicates(subset=["name", "year", "CapBefore"], keep="first")
df = df.drop_duplicates(subset=["name", "year", "CapAfter"], keep="first")

df = df.drop_duplicates(subset=["ExtOrdGMDate", "name"], keep="first")


df = df.sort_values(by=["name", "ExtOrdGMDate"])
df = df[
    [
        "name",
        "year",
        "Firm",
        "CapAfter",
        "CapBefore",
        "ExtOrdGMDate",
        "Revaluation",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "JustRevaluation",
        "Hybrid",
        "%CapRaised",
        "%PremiumCapRaising",
        "%ROCapRaising",
        "%SavingCapRaising",
    ]
]
df = df[(df.year > 1382) & (df.year < 1399)]
df.head()

# %%
pdf = pd.read_csv(path + "Stocks_Prices_1399-07-25.csv")
pdf.loc[pdf.name.str[-1] == " ", "name"] = pdf.loc[pdf.name.str[-1] == " "].name.str[
    :-1
]
pdf.loc[pdf.name.str[0] == " ", "name"] = pdf.loc[pdf.name.str[0] == " "].name.str[1:]
pdf["name"] = pdf["name"].apply(lambda x: convert_ar_characters(x))
pdf.jalaliDate = pdf.jalaliDate.apply(vv)
pdf = pdf.sort_values(by=["name", "date"])
pdf = pdf[
    [
        "jalaliDate",
        "date",
        "name",
        "title",
        "stock_id",
        "group_name",
        "group_id",
        "baseVol",
        "value",
        "volume",
        "quantity",
    ]
]
pdf = pdf.merge(df2, on=["stock_id", "date"], how="left")

# pdf['Firm'] = ''
# pdf.loc[pdf.title.str.contains("\("),'Firm'] = pdf[pdf.title.str.contains("\(")]['title'].str.split("\(", n = 1, expand = True)[0]
# firmsymbol = pdf[['name','Firm']].drop_duplicates()


# %%
gg = pdf.groupby(["name"])
pdf["close"] = gg["close"].fillna(method="ffill")
pdf["High"] = gg["High"].fillna(method="ffill")
pdf["Low"] = gg["Low"].fillna(method="ffill")
pdf["Open"] = gg["Open"].fillna(method="ffill")
pdf["Last"] = gg["Last"].fillna(method="ffill")
pdf.loc[pdf.volume == 0, "Volume"] = 0

#%%
df2 = pd.read_csv(path + "InsInd_1399-05-09" + ".csv")
# df2["Name"] = df2["Name"].apply(lambda x: convert_ar_characters(x))
df2.Date = df2.Date.apply(vv)
df2 = df2.rename(columns={"ID": "stock_id", "Date": "date"}).drop(
    columns=["Unnamed: 0", "Name"]
)
print(len(pdf), len(df2))

pdf = pdf.merge(df2, on=["stock_id", "date"], how="left")
print(len(pdf))


# %%
mdf = pd.DataFrame()
mdf = mdf.append(pdf)
mdf = mdf[mdf.volume != 0]
JalaliDates = list(set(mdf.jalaliDate))
JalaliDates.sort()
t = list(range(len(JalaliDates)))
mapingdict = dict(zip(JalaliDates, t))
mdf["t"] = mdf["jalaliDate"].map(mapingdict)


# %%
mapingdict = dict(zip(JalaliDates, t))

df["t"] = df["ExtOrdGMDate"].map(mapingdict)
tIndex = pd.DataFrame(list(mapingdict.keys()), columns=[0])
for i in set(df[df.t.isnull()].ExtOrdGMDate):
    mapingdict[i] = tIndex[tIndex[0] >= i].index[0]
df["t"] = df["ExtOrdGMDate"].map(mapingdict)


# %%
data = pd.DataFrame()
ndf = pd.DataFrame()
NotCapitalData = []
gg = mdf.groupby("name")
for symbol in list(gg.groups.keys()):
    print(symbol)
    d = gg.get_group(symbol)
    if len(d) < 30:
        continue
    t = df[df.name == symbol]
    if len(t) == 0:
        NotCapitalData.append(symbol)
        continue
    g = pd.DataFrame()
    g = g.append(d)
    g["CapBefore"] = np.nan
    g["CapAfter"] = np.nan
    g["ExtOrdGMDate"] = np.nan
    g["Event"] = np.nan
    g["JustRO"] = np.nan
    g["JustSaving"] = np.nan
    g["JustPremium"] = np.nan
    g["Hybrid"] = np.nan
    g["Revaluation"] = np.nan
    nEvent = 0
    for date in t.ExtOrdGMDate:

        Day = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].ExtOrdGMDate.iloc[0]
        CapBefore = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].CapBefore.iloc[
            0
        ]
        CapAfter = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].CapAfter.iloc[0]
        JustRO = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].JustRO.iloc[0]
        JustSaving = df[
            (df.name == symbol) & (df.ExtOrdGMDate == date)
        ].JustSaving.iloc[0]
        JustPremium = df[
            (df.name == symbol) & (df.ExtOrdGMDate == date)
        ].JustPremium.iloc[0]
        Hybrid = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].Hybrid.iloc[0]
        Revaluation = df[
            (df.name == symbol) & (df.ExtOrdGMDate == date)
        ].Revaluation.iloc[0]
        mark = 0
        #         print(g.jalaliDate.iloc[0],date)
        if (date >= g.jalaliDate.iloc[0]) and (date < g.jalaliDate.iloc[-1]):
            nEvent += 1
            mark = 1
            g.loc[g.jalaliDate >= date, "ExtOrdGMDate"] = Day
            g.loc[g.jalaliDate >= date, "CapBefore"] = CapBefore
            g.loc[g.jalaliDate >= date, "CapAfter"] = CapAfter
            g.loc[g.jalaliDate >= date, "Event"] = g.loc[g.jalaliDate >= date].t.iloc[0]
            g.loc[g.jalaliDate >= date, "JustRO"] = JustRO
            g.loc[g.jalaliDate >= date, "JustSaving"] = JustSaving
            g.loc[g.jalaliDate >= date, "JustPremium"] = JustPremium
            g.loc[g.jalaliDate >= date, "Hybrid"] = Hybrid
            g.loc[g.jalaliDate >= date, "Revaluation"] = Revaluation
            if nEvent == 1:
                g.loc[g.jalaliDate < date, "ExtOrdGMDate"] = Day
                g.loc[g.jalaliDate < date, "CapBefore"] = CapBefore
                g.loc[g.jalaliDate < date, "CapAfter"] = CapAfter
                g.loc[g.jalaliDate < date, "Event"] = g.loc[
                    g.jalaliDate >= date
                ].t.iloc[0]
                g.loc[g.jalaliDate < date, "JustRO"] = JustRO
                g.loc[g.jalaliDate < date, "JustSaving"] = JustSaving
                g.loc[g.jalaliDate < date, "JustPremium"] = JustPremium
                g.loc[g.jalaliDate < date, "Hybrid"] = Hybrid
                g.loc[g.jalaliDate < date, "Revaluation"] = Revaluation

        if mark == 1:
            ndf = ndf.append(df[(df.name == symbol) & (df.ExtOrdGMDate == date)])
    if mark == 1:
        data = data.append(g)


# %%
ndf.to_excel(path + "SDate.xlsx", index=False)

#%%


# %%
#
data2 = data.sort_values(by=["name", "t"], ascending=False).reset_index(drop=True)
gg = data2.groupby("name")
data2["Event"] = gg["Event"].fillna(method="ffill")


# %%
data = data2.sort_values(by=["name", "t"])
# data['Period'] = data['t'] - data['Event']


# %%

index = pd.read_excel(path + "IRX6XTPI0009.xls")[["<COL14>", "<CLOSE>"]].rename(
    columns={"<COL14>": "jalaliDate", "<CLOSE>": "Index"}
)
# index["Market_return"] = index["Index"].pct_change(periods=1) * 100
# index = DriveYearMonthDay(index)
pdf.jalaliDate = pdf.jalaliDate.astype(int)
index = index[index.jalaliDate >= pdf.jalaliDate.min()]
n = path + "RiskFree rate.xlsx"
rf = pd.read_excel(n)
rf = rf.rename(columns={"Unnamed: 2": "Year"})
rf["YM"] = rf["YM"].astype(str)
rf["YM"] = rf["YM"] + "00"
rf["YM"] = rf["YM"].astype(int)
index["RiskFree"] = np.nan
index["jalaliDate"] = index["jalaliDate"].astype(int)
for i in rf.YM:
    index.loc[index.jalaliDate >= i, "RiskFree"] = (
        rf.loc[rf["YM"] == i].iloc[0, 1] / 356
    )


# %%
data = data.merge(index, on="jalaliDate")

# %%
data = data.sort_values(by=["name", "t"]).reset_index(drop=True)
data = data[~data.High.isnull()]
gg = data.groupby("name")
data["Market_return"] = gg["Index"].pct_change(periods=1) * 100
data = data[~data.Market_return.isnull()]
data = data.rename(columns={"close": "close_price"})
#%%
def divide_to_mean(g):
    print(g.name, end="\r", flush=True)
    g = g / g.rolling(60, 1).mean()
    return g


gg = data.groupby("name")
data["RelVolume"] = gg.volume.apply(divide_to_mean)

#%%
path1 = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
df = pd.read_excel(path1 + "Factors-Daily" + ".xlsx")
for t in ["SMB", "HML", "Winner_Loser"]:
    print(t)
    df[t + "Index"] = df[t] / 100 + 1
    df[t + "Index"] = df[t + "Index"].rolling(len(df), 1).apply(np.prod)

for t in ["SMB", "HML", "Winner_Loser"]:
    print(t)
    mapingdict = dict(zip(df.date, df[t + "Index"]))
    data[t] = data.date.map(mapingdict)
    gg = data.groupby("name")
    data[t] = gg[t].pct_change(periods=1) * 100

# %%
data.isnull().sum().to_frame()
data = data.dropna()

n = path + "RawDataBeforeAb.parquet"

data.to_parquet(n)


#%%
data = pd.read_parquet(path + "RawDataBeforeAb.parquet")

# %%
def ABnormal(g, Rlag):
    lag = 121 + Rlag
    print(g.name)
    a = pd.DataFrame()
    a = a.append(g)
    a = a[~a.ER.isnull()]
    a = a.reset_index(drop=True).reset_index().rename(columns={"index": "Period"})
    a["Period"] = a["Period"].astype(int)
    a["AbnormalReturn"] = np.nan
    a["AbnormalReturn_Market"] = np.nan
    a["AbnormalReturn_WithoutAlpha"] = np.nan
    a["AbnormalReturn_4Factor"] = np.nan

    a["EPeriod"] = np.nan
    a["nEvent"] = np.nan
    a["Beta_CAPM"] = np.nan
    a["Alpha_CAPM"] = np.nan

    a["betaM_FOUR"] = np.nan
    a["betaS_FOUR"] = np.nan
    a["betaH_FOUR"] = np.nan
    a["betaW_FOUR"] = np.nan
    a["Alpha_FOUR"] = np.nan
    nEvent = 0
    for i in a[a.Event == a.t]["Period"]:
        nEvent += 1
        tempt = pd.DataFrame()
        tempt = a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag))]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "EPeriod"] = (
            tempt["Period"] - i
        )
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "nEvent"] = nEvent

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "JustRO"] = a[
            a.Period == i
        ]["JustRO"].iloc[0]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "JustSaving"] = a[
            a.Period == i
        ]["JustSaving"].iloc[0]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "JustPremium"] = a[
            a.Period == i
        ]["JustPremium"].iloc[0]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Hybrid"] = a[
            a.Period == i
        ]["Hybrid"].iloc[0]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Revaluation"] = a[
            a.Period == i
        ]["Revaluation"].iloc[0]

        if len(a.loc[a.EPeriod < -1 * Rlag]) < 30:
            continue

        alpha, beta = ols(a.loc[a.EPeriod < -1 * Rlag])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn"
        ] = tempt["Return"] - (tempt["RiskFree"] + alpha + beta * tempt["EMR"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha",
        ] = tempt["Return"] - (tempt["RiskFree"] + beta * tempt["EMR"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn_Market"
        ] = tempt["Return"] - (tempt["RiskFree"] + tempt["EMR"])

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_CAPM"] = alpha

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_CAPM"] = beta

        alpha, betaM, betaS, betaH, betaW = ols4(a.loc[a.EPeriod < -1 * Rlag])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn_4Factor"
        ] = tempt["Return"] - (
            tempt["RiskFree"]
            + alpha
            + betaM * tempt["EMR"]
            + betaS * tempt["SMB"]
            + betaH * tempt["HML"]
            + betaW * tempt["Winner_Loser"]
        )

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_FOUR"] = alpha

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "betaM_FOUR"] = betaM
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "betaS_FOUR"] = betaS

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "betaH_FOUR"] = betaH

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "betaW_FOUR"] = betaW

    return a[(~a["EPeriod"].isnull())]


def ols(tempt):
    y, x = "ER", "EMR"
    model = sm.OLS(tempt[y], sm.add_constant(tempt[x])).fit()
    beta = model.params[1]
    alpha = model.params[0]
    return alpha, beta


def ols4(tempt):
    y, x = "ER", ["EMR", "SMB", "HML", "Winner_Loser"]
    model = sm.OLS(tempt[y], sm.add_constant(tempt[x])).fit()
    betaW = model.params[4]
    betaH = model.params[3]
    betaS = model.params[2]
    betaM = model.params[1]
    alpha = model.params[0]
    return alpha, betaM, betaS, betaH, betaW


#%%
ARdata = pd.DataFrame()
ARdata = ARdata.append(data)
ARdata["Return"] = ARdata.groupby("name")["close_price"].pct_change(periods=1) * 100
ARdata["ER"] = ARdata["Return"] - ARdata["RiskFree"]
ARdata["EMR"] = ARdata["Market_return"] - ARdata["RiskFree"]
gg = ARdata.groupby("name")


## Lag

ARdata = gg.apply(ABnormal, Rlag=20).reset_index(drop=True)

##
ARdata = ARdata.sort_values(by=["name", "t"])
ARdata.isnull().sum()


#%%
Data = pd.DataFrame()
Data = Data.append(ARdata)
Data = Data.reset_index(drop=True)
Data = Data.rename(columns={"ER": "EReturn"})
Data["Amihud"] = abs(Data["Return"]) / Data["Volume"]
Data = Data.loc[(Data.EPeriod >= -20) & (Data.EPeriod <= 100)]

Data["NetInd"] = Data["ind_buy_volume"] - Data["ind_sell_volume"]
Data["TotalInd"] = Data["ind_buy_volume"] + Data["ind_sell_volume"]
Data["NetIns"] = Data["ins_buy_volume"] - Data["ins_sell_volume"]
Data["TotalIns"] = Data["ins_buy_volume"] + Data["ins_sell_volume"]

Data["IndlImbalance"] = Data["NetInd"].divide(Data["TotalInd"])
Data["InslImbalance"] = Data["NetIns"].divide(Data["TotalIns"])


gg = Data.groupby(["name", "nEvent"])
Data["CAR"] = gg["AbnormalReturn"].cumsum()
Data["CAR_Market"] = gg["AbnormalReturn_Market"].cumsum()
Data["CAR_WithoutAlpha"] = gg["AbnormalReturn_WithoutAlpha"].cumsum()
Data["CAR_4Factor"] = gg["AbnormalReturn_4Factor"].cumsum()
Data["RaiseType"] = np.nan
Data.loc[Data.JustRO == 1, "RaiseType"] = "JustRO"
Data.loc[Data.JustSaving == 1, "RaiseType"] = "JustSaving"
Data.loc[Data.JustPremium == 1, "RaiseType"] = "JustPremium"
Data.loc[Data.Hybrid == 1, "RaiseType"] = "Hybrid"
Data.loc[Data.Revaluation == 1, "RaiseType"] = "Revaluation"


#%%
d = path + "CapitalRaise.parquet"
Data.to_parquet(d)

# %%

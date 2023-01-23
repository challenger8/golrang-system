import pandas as pd

import plotly.express as px
from sklearn.cluster import KMeans
import seaborn as sns


def preprocessing(data:pd.DataFrame()):
    data['date'] = pd.to_datetime(data['date'])
    data['weekday'] = data.date.dt.weekday
    data['weekday'] = data['weekday'].apply(lambda x: int(x))
    data['dayofweek'] = data.date.dt.day_name()
    data['total_purchase'] = data.total_purchase.fillna(0)
    df = pd.DataFrame(data.groupby(pd.Grouper(key='date',
                                              freq='1D'))['total_purchase'].count()).reset_index()
    df['dayofweek'] = df.date.dt.day_name()
    return df


def quest1(data: pd.DataFrame()):
    df=preprocessing(data)
    df['dayofweek'] = df.date.dt.day_name()
    fin1 = pd.DataFrame(df.groupby('dayofweek')['total_purchase'].mean())
    fin1['std'] = df.groupby('dayofweek')['total_purchase'].std().values
    fin1 = fin1.reset_index()
    fin1 = fin1.rename(columns={"total_purchase": "mean"})
    return fin1


def holiday(x):
    if x in ['Friday', 'Thursday']:
        return 'weekend'
    else:
        return 'working day'


def quest2(data: pd.DataFrame()):
    df = preprocessing(data)
    df['weekend'] = df['dayofweek'].apply(lambda x: holiday(x))
    plot = df.groupby(['dayofweek', 'weekend']).mean().reset_index()
    fig = px.bar(plot, x="dayofweek", y="total_purchase",
                 color='weekend', barmode='group',
                 height=400)
    # fig.show()
    return fig


def quest3(df: pd.DataFrame(), n_cluster):
    data = df
    snapshot = data["date"].max()  # the last day is our max date
    snapshot = snapshot + pd.Timedelta(days=1)
    customer_group = data.groupby(
        "user_id")  # grouping the customer id's to see every single customer's activity on r, f , m
    recency = (snapshot - customer_group[
        "date"].max())  # the last day of grouped customer's transaction is captured with .max()
    frequency = customer_group["total_purchase"].nunique()  # how many times the customer made transactions?
    monetary = customer_group["total_purchase"].sum()
    tenure = snapshot - customer_group[
        "date"].min()  # the first day of grouped customer's transaction is captured with .min()
    rfm = rfm = pd.DataFrame()  # opened a new rfm dataframe
    rfm["Recency"] = recency.dt.days  # FORMAT CHANGE: timedelta64 to integer
    rfm["Frequency"] = frequency
    rfm["Monetary"] = monetary
    rfm["Tenure"] = tenure.dt.days
    X = rfm.values
    # n_cluster = 5
    model = KMeans(n_clusters=n_cluster, random_state=28)
    y = model.fit_predict(X)

    rfm["Segment"] = y
    # return rfm.drop(['Tenure'], axis=1).groupby("Segment").mean()
    return rfm



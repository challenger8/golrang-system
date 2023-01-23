import streamlit as st
from Questions import *
import matplotlib.pyplot as plt


def main():
    df = load_data()
    page = st.sidebar.selectbox("Choose a page", ["question1", "question2", 'question3'])

    if page == "question1":
        st.header("This is about answer about question 1")
        st.write(quest1(df))
    elif page == "question2":
        st.header("This is about answer about question 2")
        st.plotly_chart(quest2(df))
    elif page == "question3":
        st.header("This is about answer about question ")
        st.header("This information about clusters RFM features")
        n_cluster = st.number_input('number of clusters', min_value=1, max_value=20, value=5, step=1)
        rfm = quest3(df, n_cluster)
        st.write(rfm.drop(['Tenure'], axis=1).groupby("Segment").mean())
        sns.set_theme()
        st.header("This plot related to visualization member of clusters ")
        # fig = plt.figure(figsize=(10, 4))
        g = sns.lmplot(
            data=rfm,
            x="Recency", y="Frequency", hue="Segment",
            height=5
        )
        st.pyplot(fig=g)

        # Use more informative axis labels than are provided by default
        g.set_axis_labels("Recency", "Frequency")


@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv("sample_data.csv")
    data['date'] = pd.to_datetime(data['date'])
    data['weekday'] = data.date.dt.weekday
    data['weekday'] = data['weekday'].apply(lambda x: int(x))
    data['dayofweek'] = data.date.dt.day_name()
    return data

# Will only run once if already cached


if __name__ == "__main__":
    main()

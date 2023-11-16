import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


# jumlah_hari_df() digunakan untuk menyiapkan jumlah_hari_df.
def create_jumlah_hari_df(df):
    jumlah_hari_df = df.resample(rule='M', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    jumlah_hari_df = jumlah_hari_df.reset_index()
    jumlah_hari_df.rename(columns={
        "instant": "hari",
        "cnt": "Total_cnt"
    }, inplace=True)
    
    return jumlah_hari_df


day_clean_df = pd.read_csv("day_clean_df.csv")

datetime_columns = ['dteday']
day_clean_df.sort_values(by="dteday", inplace=True)
day_clean_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_clean_df[column] = pd.to_datetime(day_clean_df[column])

# Memilih data day_df berdasarkan tahun 2011
bike_2011 = day_clean_df[(day_clean_df['dteday'] < "2012-01-01")]

monthly_2011 = bike_2011.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
})
monthly_2011.index = monthly_2011.index.strftime('%B') #mengubah format order date menjadi nama bulan
 
monthly_2011 = monthly_2011.reset_index()
monthly_2011.rename(columns={
    "cnt": "Total_cnt"
}, inplace=True)


# Memilih data day_df berdasarkan tahun 2012
bike_2012 = day_clean_df[(day_clean_df['dteday'] > "2011-12-31")]

monthly_2012 = bike_2012.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
})
monthly_2012.index = monthly_2012.index.strftime('%B') #mengubah format order date menjadi nama bulan
 
monthly_2012 = monthly_2012.reset_index()
monthly_2012.rename(columns={
    "cnt": "Total_cnt"
}, inplace=True)


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    


jumlah_hari_df = create_jumlah_hari_df(day_clean_df)

st.header('Proyek Dicoding Collection Dashboard :sparkles:')

st.subheader('Rental Bikes')
 
col1, col2 = st.columns(2)
 
with col1:
    total_hari = jumlah_hari_df.hari.sum()
    st.metric("Total day", value=total_hari)
 
with col2:
    total_rental = jumlah_hari_df.Total_cnt.sum()
    st.metric("Count of total Rental Bikes", value=total_rental)

# Bicycle Rental performance per month in 2 years
st.subheader("Bicycle Rental performance per month in 2 years")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))
 
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
col1, col2 = st.columns(2)


sns.lineplot(x="dteday", y="Total_cnt", data=monthly_2011.head(12), marker='o', ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Total rental Bikes per Month (2011)", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)
ax[0].tick_params(axis ='x', rotation=30)

sns.lineplot(x="dteday", y="Total_cnt", data=monthly_2012.head(12), marker='o', ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Total rental Bikes per Month (2012)", loc="center", fontsize=15)
ax[1].tick_params(axis ='y', labelsize=12)
ax[1].tick_params(axis ='x', rotation=30)

plt.suptitle("Count of total rental Bikes per Month", fontsize=30)
st.pyplot(fig)



# Grafik berdasarkan weathersit
st.subheader('Optimal weather conditions for running a Bicycle Rental business')

weathersit2011_df = bike_2011.groupby(by="weathersit").cnt.sum().reset_index()
weathersit2011_df.rename(columns={
    "cnt": "Total_cnt"
}, inplace=True)

colors_ = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    x="Total_cnt",
    y="weathersit",
    data=weathersit2011_df.sort_values(by="Total_cnt", ascending=False),
    palette=colors_
)

plt.title("Count of total rental Bikes by weathersit in 2011", loc="center", fontsize=30)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
st.pyplot(fig)


weathersit2012_df = bike_2012.groupby(by="weathersit").cnt.sum().reset_index()
weathersit2012_df.rename(columns={
    "cnt": "Total_cnt"
}, inplace=True)

colors_ = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    x="Total_cnt",
    y="weathersit",
    data=weathersit2012_df.sort_values(by="Total_cnt", ascending=False),
    palette=colors_
)

plt.title("Count of total rental Bikes by weathersit in 2012", loc="center", fontsize=30)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
st.pyplot(fig)



st.subheader('Count of Rental Bikes per Season')

# Total cnt berdasarkan season 2011
season2011_df = bike_2011.groupby(by="season").cnt.sum().reset_index()
season2011_df.rename(columns={
    "cnt": "Total_cnt"
}, inplace=True)

# Total cnt berdasarkan season 2012
season2012_df = bike_2012.groupby(by="season").cnt.sum().reset_index()
season2012_df.rename(columns={
    "cnt": "Total_cnt"
}, inplace=True)


col1, col2 = st.columns(2)
 
with col1:
    

    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="Total_cnt", 
        x="season",
        data=season2011_df.sort_values(by="Total_cnt", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Count of total rental Bikes by Season in 2011", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="Total_cnt", 
        x="season",
        data=season2012_df.sort_values(by="Total_cnt", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Count of total rental Bikes by Season in 2012", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)


# Count of total Rental Bikes per Season in 2011-2012
st.subheader('Count of total Rental Bikes per Season in 2011-2012')
col1, col2, col3, col4= st.columns(4)

with col1:
    st.metric("Fall", value=1061129)

with col2:
    st.metric("Summer", value=918589)

with col3:
    st.metric("Winter", value=841613)

with col4:
    st.metric("Springer", value=471348)


season_df = day_clean_df.groupby(by="season").cnt.sum().reset_index()
season_df.rename(columns={
    "cnt": "Total_cnt"
}, inplace=True)

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="Total_cnt", 
    y="season",
    data=season_df.sort_values(by="Total_cnt", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Count of total Rental Bikes per Season in 2011-2012", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
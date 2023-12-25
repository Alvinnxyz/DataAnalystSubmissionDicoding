import streamlit as st
import pandas as pd
import calendar
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('df.csv')
Aotizhongxin=pd.read_csv('content/PRSA_Data_Aotizhongxin_20130301-20170228.csv')
Changping=pd.read_csv('content/PRSA_Data_Changping_20130301-20170228.csv')
Dingling=pd.read_csv('content/PRSA_Data_Dingling_20130301-20170228.csv')
Dongsi=pd.read_csv('content/PRSA_Data_Dongsi_20130301-20170228.csv')
Guanyuan=pd.read_csv('content/PRSA_Data_Guanyuan_20130301-20170228.csv')
Gucheng=pd.read_csv('content/PRSA_Data_Gucheng_20130301-20170228.csv')
Huairou=pd.read_csv('content/PRSA_Data_Huairou_20130301-20170228.csv')
Nongzhanguan=pd.read_csv('content/PRSA_Data_Nongzhanguan_20130301-20170228.csv')
Shunyi=pd.read_csv('content/PRSA_Data_Shunyi_20130301-20170228.csv')
Tiantan=pd.read_csv('content/PRSA_Data_Tiantan_20130301-20170228.csv')
Wanliu=pd.read_csv('content/PRSA_Data_Wanliu_20130301-20170228.csv')
Wanshouxigong=pd.read_csv('content/PRSA_Data_Wanshouxigong_20130301-20170228.csv')
data = [Aotizhongxin, Changping, Dingling, Dongsi, Guanyuan, Gucheng, Huairou, 
            Nongzhanguan, Shunyi, Tiantan, Wanliu, Wanshouxigong]
# delete missing values 
for df_station in data:
    df_station.dropna(axis=0, inplace=True)

# Inisialisasi DataFrame 
percentage_pm25_100_by_station = pd.DataFrame(columns=['Station', 'Percentage'])

# Calculate percentage by station
for df_station in data:
    station_name = df_station['station'].iloc[0]
    pm25_100 = df_station[df_station['PM2.5'] > 100]['PM2.5'].count()
    total_data = df_station['PM2.5'].count()
    percentage = (pm25_100 / total_data) * 100
    percentage_pm25_100_by_station = pd.concat([percentage_pm25_100_by_station,
                                                pd.DataFrame({'Station': [station_name], 'Percentage': [percentage]})])


# Function to calculate PM2.5 > 100 percentage by year
def calculate_percentage_by_year(df):
    pm25_100_by_year = df[df['PM2.5'] > 100].groupby('year')['PM2.5'].count()
    total_data_by_year = df.groupby('year')['PM2.5'].count()
    percentage_pm25_100_by_year = (pm25_100_by_year / total_data_by_year) * 100
    result_df = percentage_pm25_100_by_year.reset_index(name='Percentage')
    return result_df

# Function to calculate PM2.5 > 100 percentage by month
def calculate_percentage_by_month(df):
    pm25_100_by_month_all = df[df['PM2.5'] > 100].groupby('month')['PM2.5'].count()
    total_data_by_month_all = df.groupby('month')['PM2.5'].count()
    percentage_pm25_100_by_month_all = (pm25_100_by_month_all / total_data_by_month_all) * 100
    percentage_pm25_100_by_month_all.index = percentage_pm25_100_by_month_all.index.map(lambda x: calendar.month_abbr[x])
    result_df_month = percentage_pm25_100_by_month_all.reset_index(name='Percentage')
    return result_df_month

# Streamlit App
st.title("PM2.5 Analysis Dashboard")

# Visualization 1: Bar Chart by Year
st.header("1. Percentage of PM2.5 > 100 by Year")
result_df_year = calculate_percentage_by_year(df)
fig_year = px.bar(result_df_year, x='year', y='Percentage', labels={'Percentage': 'PM2.5 > 100 Percentage'})
st.plotly_chart(fig_year)

# Visualization 2: Line Chart by Month
st.header("2. Percentage of PM2.5 > 100 by Month")
result_df_month = calculate_percentage_by_month(df)
fig_month = px.line(result_df_month, x='month', y='Percentage', labels={'Percentage': 'PM2.5 > 100 Percentage'})
st.plotly_chart(fig_month)

# Visualization 3: Bar Plot by Station
percentage_pm25_100_by_station = percentage_pm25_100_by_station.sort_values(by='Percentage', ascending=False)
st.header("3. Percentage of PM2.5 > 100 by Station")
plt.figure(figsize=(12, 8))
barplot = sns.barplot(x='Percentage', y='Station', data=percentage_pm25_100_by_station, palette='viridis')
plt.title('Percentage of PM2.5 > 100 at Each Station', fontsize=16)
plt.xlabel('Percentage (%)', fontsize=14)
plt.ylabel('Station', fontsize=14)

# Add value annotations
for index, value in enumerate(percentage_pm25_100_by_station['Percentage']):
    if value <= 50:
        barplot.text(value, index, f'{value:.2f}%', ha='left', va='center', fontsize=12, color='black')
    else:
        barplot.text(value, index, f'{value:.2f}%', ha='right', va='center', fontsize=12, color='black')

# Extend x-axis to 35 for better visualization
plt.xlim(0, 35)
# Display the plot
st.pyplot(plt)


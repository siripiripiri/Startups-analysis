import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.linear_model import LinearRegression

# Load the dataset
file_path = r'./startups_dset.csv'
data = pd.read_csv(file_path)

# Set up the Streamlit app
st.title("Startup Analysis Dashboard")
# Convert the 'Amount' column to strings
data['Amount'] = data['Amount'].astype(str)
# Clean the 'Amount' column by removing dollar signs and commas
data['Amount'] = data['Amount'].str.replace('[\$,]', '', regex=True)
# Convert the cleaned 'Amount' column to numeric
data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

st.sidebar.header("Choose your filter:")
years = st.sidebar.multiselect("Pick your Year Funded", data["Year_Funded"].unique())
rounds = st.sidebar.multiselect("Pick the Funding Round", data["Round/Series"].unique())
locations = st.sidebar.multiselect("Pick the Location", data["Location"].unique())

filtered_data = data
if years:
    filtered_data = filtered_data[filtered_data["Year_Funded"].isin(years)]
if rounds:
    filtered_data = filtered_data[filtered_data["Round/Series"].isin(rounds)]
if locations:
    filtered_data = filtered_data[filtered_data["Location"].isin(locations)]


# Top 10 startups by revenue over the last 5 years
#top_10_startups = data.sort_values(by='Amount', ascending=False).head(10)
# st.subheader("Top 10 Startups by Revenue")
# st.write(top_10_startups)

# Metrics section
total_investment = float(filtered_data['Amount'].sum())
average_investment = float(filtered_data['Amount'].mean())
max_investment = float(filtered_data['Amount'].max())
min_investment = float(filtered_data['Amount'].min())

st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 18px;  /* Customize the font size here */
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

total1, total2, total3, total4 = st.columns(4)
with total1:
    st.info('Total Investment', icon="💲")
    st.metric("Total Investment", f"{total_investment:,.0f}")
with total2:
    st.info('Most frequent Investment', icon="💹")
    st.metric("Average Investment", f"{average_investment:,.0f}")
with total3:
    st.info('Average Investment', icon="💰")
    st.metric("Max Investment", f"{max_investment:,.0f}")
with total4:
    st.info('Central Earnings', icon="💸")
    st.metric("Min Investment", f"{min_investment:,.0f}")


# Example: Location-wise distribution of startups
st.subheader("Location-wise Distribution of Startups")
location_counts = data['Location'].value_counts()
st.bar_chart(location_counts)

st.title('Count of Companies in Each Industry')

# Calculate industry counts for the top 20 records
top_20_data = data.head(20)
industry_counts = top_20_data['Industry'].value_counts()

# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x=industry_counts.index, y=industry_counts.values)
plt.title('Count of Companies in Each Industry (Top 20)')
plt.xlabel('Industry')
plt.ylabel('Count')
plt.xticks(rotation=90)

# Show the plot in Streamlit
st.pyplot(plt)

# Example: Funding trends by year
st.subheader("Funding Trends by Year")
funding_by_year = data.groupby('Year_Funded')['Amount'].sum()
st.line_chart(funding_by_year)



# st.sidebar.header("Choose your filter:")
# yr = st.sidebar.multiselect("Pick your Year", data["Year"].unique())
# if not yr:
#     df2 = data.copy()
# else:
#     df2 = data[data["Round/Series"].isin(yr)]

# rs = st.sidebar.multiselect("Pick the Funding Round", df2["Round/Series"].unique())
# if not rs:
#     df3 = df2.copy()
# else:
#     df3 = df2[df2["Round/Series"].isin(rs)]

# loc = st.sidebar.multiselect("Pick the City", df3["Location"].unique())
# if not loc:
#     df4 = df3.copy()
# else:
#     df4 = df3[df3["Location"].isin(loc)]




# st.sidebar.header("Choose your filter:")
# yr = st.sidebar.multiselect("Pick your Year", data["Year_Funded"].unique())
# rs = st.sidebar.multiselect("Pick the Funding Round", data["Round/Series"].unique())
# loc = st.sidebar.multiselect("Pick the City", data["Location"].unique())

#fintech companies
fintech_data = data[data['Industry'] == 'Fintech']

# Filter data for the years 2018 to 2023
years = list(range(2018, 2024))
fintech_data = fintech_data[fintech_data['Year_Funded'].isin(years)]

# Group data by year and calculate total revenue
revenue_by_year = fintech_data.groupby('Year_Funded')['Amount'].sum().reset_index()

# Create a line chart using Plotly Express
fig = px.line(revenue_by_year, x='Year_Funded', y='Amount', title='Fintech Revenue Analysis (2018-2023)')
fig.update_xaxes(type='category')  # Ensure years are treated as categories
fig.update_traces(mode='lines+markers')  # Add markers at data points

# Display the chart in your Streamlit app
st.plotly_chart(fig)

year_2020_data = data[data['Year_Funded'] == 2020]

sector_funding_2020 = year_2020_data.groupby('Industry')['Amount'].sum().reset_index()

fig = px.bar(sector_funding_2020, x='Industry', y='Amount', title='Startup Funding by Sector in 2020')
fig.update_xaxes(categoryorder='total descending')  # Sort sectors by total funding amount in descending order

fig.update_traces(marker_color='blue')  
st.plotly_chart(fig)

sector_counts = data['Industry'].value_counts().reset_index()
sector_counts.columns = ['Industry', 'Startup Count']

# Create a bar chart using Plotly Express
fig = px.bar(sector_counts, x='Industry', y='Startup Count', title='Startup Counts by Sector')
fig.update_xaxes(categoryorder='total descending')  # Sort sectors by the count of startups in descending order


fig.update_traces(marker_color='green')  # You can change the bar color

st.plotly_chart(fig)


#EV
#  # Change this to the industry you want to analyze
industry_name = 'EV'
industry_data = data[data['Industry'] == industry_name]

funding_by_year = industry_data.groupby('Year_Funded')['Amount'].sum().reset_index()

fig = px.line(funding_by_year, x='Year_Funded', y='Amount', title=f'Funding Evolution for EVs Over Time')
fig.update_xaxes(type='category')
fig.update_traces(mode='lines+markers') 

st.plotly_chart(fig)


#prediction
selected_years = list(range(2018, 2024))
filtered_data = data[data['Year_Funded'].isin(selected_years)]

# Create a linear regression model
model = LinearRegression()

# Create a new DataFrame to store the predictions
predictions_data = filtered_data.copy()

# Group data by startup and year and calculate the total funding for each year
startup_yearly_revenue = filtered_data.groupby(['Company Name', 'Year_Funded'])['Amount'].sum().reset_index()

# Sort the data by startup and year
startup_yearly_revenue.sort_values(['Company Name', 'Year_Funded'], inplace=True)

# Initialize a dictionary to store the predictions
predictions = {}

# Iterate through the data to predict revenue for each row
for startup in startup_yearly_revenue['Company Name'].unique():
    startup_data = startup_yearly_revenue[startup_yearly_revenue['Company Name'] == startup]
    
    X = startup_data['Year_Funded'].values.reshape(-1, 1)
    y = startup_data['Amount'].values
    
    model.fit(X, y)
    
    # Predict revenue for each year
    predicted_revenue = model.predict(X)
    
    # Store the predictions in the dictionary
    for i, year in enumerate(startup_data['Year_Funded']):
        predictions[(startup, year)] = predicted_revenue[i]

# Add a new column for predicted revenue
predictions_data['Predicted_Revenue'] = [predictions.get((row['Company Name'], row['Year_Funded']), 0) for _, row in predictions_data.iterrows()]

# Display the predictions as a table
st.subheader("Predicted Revenue for Each Row in the Dataset")
st.write(predictions_data[['Company Name', 'Year_Funded', 'Amount', 'Predicted_Revenue']])

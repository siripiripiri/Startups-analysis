import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Cookie Bytes", page_icon=":cookie:",layout="wide")
# Load the dataset
file_path = r'./finally.csv'
data = pd.read_csv(file_path)

# Set up the Streamlit app
st.title(":trophy: Startup Analysis Dashboard")
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
    st.info('Overall Total Investment', icon="💲")
    st.metric("Total Investment", f"{total_investment:,.0f}")
with total2:
    st.info('Most frequent Investment', icon="💹")
    st.metric("Average Investment", f"{average_investment:,.0f}")
with total3:
    st.info('Total Maximum Investment', icon="💰")
    st.metric("Max Investment", f"{max_investment:,.0f}")
with total4:
    st.info('Total Minimum Investment', icon="💸")
    st.metric("Min Investment", f"{min_investment:,.0f}")


# Top 10 Startups by Revenue
top_10_startups = filtered_data.groupby('Company Name')['Amount'].sum().sort_values(ascending=False).head(10)
st.subheader('Top 10 Startups by Revenue')
st.bar_chart(top_10_startups)
# Founded by Year
founded_by_year = filtered_data['Year_Funded'].value_counts().sort_index()
st.subheader('Founded by Year')
st.line_chart(founded_by_year)

cl1, cl2 = st.columns((2))
with cl1:
    #Location-wise distribution of startups
    st.subheader("Location-wise Distribution of Startups")
    location_counts = data['Location'].value_counts()
    st.bar_chart(location_counts)
    if st.button("Download Location-wise Distribution as CSV"):
        # Create a DataFrame from the location counts
        location_counts_df = pd.DataFrame({'Location': location_counts.index, 'Count': location_counts.values})

        # Save the location-wise distribution as a CSV file
        location_counts_df.to_csv('location_distribution.csv', index=False)

        # Provide a download button for the CSV file
        csv_data = location_counts_df.to_csv(index=False)
        st.download_button(
            "Download Location-wise Distribution CSV",
            data=csv_data,
            file_name="location_distribution.csv",
            mime="text/csv",
            key='location_distribution_button',
            help='Click here to download the data as a CSV file'
        )
with cl2:
    # Location-wise Distribution of Top 100 Startups
    top_100_startups = filtered_data.groupby('Location')['Company Name'].count().sort_values(ascending=False).head(100)
    st.subheader('Location-wise Distribution of Top 100 Startups')
    st.bar_chart(top_100_startups)
    csv_data = top_100_startups.to_csv(index=False)
    st.download_button(
        "Download Top 100 Startups CSV",
        data=csv_data,
        file_name="top_100_startups.csv",
        mime="text/csv",
        key='top_100_startups_button',
        help='Click here to download the data as a CSV file'
    )


# Group startups by funding round and year
# grouped_data = filtered_data.groupby(['Round/Series', 'Year_Funded']).count().reset_index()
# # Calculate the number of startups in each funding round for each year
# pivot_table = pd.pivot_table(grouped_data, values='Company Name', index='Year_Funded', columns='Round/Series', aggfunc='count', fill_value=0)
# # Create a bar chart to visualize the distribution of funding rounds
# st.subheader("Distribution of Funding Rounds Over the Years")
# st.bar_chart(pivot_table)

multiselect_key = "selected_industries_" + str(id(data))
slider_key = "amount_range_" + str(id(data))

# Create a multiselect widget to select specific industries
selected_industries = st.multiselect("Select Industries", data['Industry'].unique(), key=multiselect_key)

# Create a range slider for the amount
min_amount, max_amount = st.slider("Select Amount Range", data['Amount'].min(), data['Amount'].max(), (data['Amount'].min(), data['Amount'].max()), key=slider_key)

# Filter the data based on user selections
filtered_data = data.copy()

if selected_industries:
    filtered_data = filtered_data[filtered_data['Industry'].isin(selected_industries)]

filtered_data = filtered_data[(filtered_data['Amount'] >= min_amount) & (filtered_data['Amount'] <= max_amount)]

# Create a chart based on filtered data
st.subheader("Startup Funding by Sector in 2020")
year_2020_data = filtered_data[filtered_data['Year_Funded'] == 2020]
sector_funding_2020 = year_2020_data.groupby('Industry')['Amount'].sum().reset_index()
fig = px.bar(sector_funding_2020, x='Industry', y='Amount')
fig.update_xaxes(categoryorder='total descending')  # Sort sectors by total funding amount in descending order
fig.update_traces(marker_color='blue')  
st.plotly_chart(fig)

sector_counts = filtered_data['Industry'].value_counts().reset_index()
sector_counts.columns = ['Industry', 'Startup Count']

# Create a bar chart for the number of startups by industry
st.subheader("Number of Startups by Industry")
fig2 = px.bar(sector_counts, x='Industry', y='Startup Count')
st.plotly_chart(fig2)

# Count of Companies in Each Industry
st.subheader("Count of Companies in Each Industry")
# Calculate industry counts for the top 20 records
top_20_data = filtered_data.head(20)
# industry_counts = top_20_data['Industry'].value_counts()
# industry_counts = filtered_data['Industry'].value_counts()
# Create a multiselect widget to allow users to select specific industries
selected_industries = st.multiselect("Select Industries", filtered_data['Industry'].unique())
# Filter the data based on selected industries
if selected_industries:
    industry_counts = filtered_data[filtered_data['Industry'].isin(selected_industries)]['Industry'].value_counts()
else:
    industry_counts = filtered_data['Industry'].value_counts()
# Create a bar chart to display the industry counts
st.bar_chart(industry_counts)
# # Create a bar plot
# plt.figure(figsize=(10, 6))
# sns.barplot(x=industry_counts.index, y=industry_counts.values)
# plt.title('Count of Companies in Each Industry (Top 20)')
# plt.xlabel('Industry')
# plt.ylabel('Count')
# plt.xticks(rotation=90)
# Show the plot in Streamlit
# st.pyplot(plt)


st.subheader("Fintech Revenue Analysis (2018-2023)")
fintech_data = data[data['Industry'] == 'Fintech']
# Filter data for the years 2018 to 2023
years = list(range(2018, 2024))
fintech_data = fintech_data[fintech_data['Year_Funded'].isin(years)] 
# Group data by year and calculate total revenue
revenue_by_year = fintech_data.groupby('Year_Funded')['Amount'].sum().reset_index() 
# Create a line chart using Plotly Express
fig = px.line(revenue_by_year, x='Year_Funded', y='Amount')
fig.update_xaxes(type='category')  # Ensure years are treated as categories
fig.update_traces(mode='lines+markers')  # Add markers at data points
# Display the chart in your Streamlit app
st.plotly_chart(fig)


# st.subheader("Startup Funding by Sector in 2020") 
# year_2020_data = data[data['Year_Funded'] == 2020]
# sector_funding_2020 = year_2020_data.groupby('Industry')['Amount'].sum().reset_index()
# fig = px.bar(sector_funding_2020, x='Industry', y='Amount')
# fig.update_xaxes(categoryorder='total descending')  # Sort sectors by total funding amount in descending order
# fig.update_traces(marker_color='blue')  
# st.plotly_chart(fig)
# sector_counts = data['Industry'].value_counts().reset_index()
# sector_counts.columns = ['Industry', 'Startup Count']
# # Create a bar chart using Plotly Express
# Create a multiselect widget to select specific industries
# Create a multiselect widget to select specific industries

# Create a chart based on filtered data
st.subheader("Startup Funding by Sector in 2020")
selected_industries = st.multiselect("Select Industries", data['Industry'].unique(), key="selected_industries")
# Create a range slider for the amount
min_amount, max_amount = st.slider("Select Amount Range", data['Amount'].min(), data['Amount'].max(), (data['Amount'].min(), data['Amount'].max()), key="amount_range")
# Filter the data based on user selections
filtered_data = data.copy()
if selected_industries:
    filtered_data = filtered_data[filtered_data['Industry'].isin(selected_industries)]
filtered_data = filtered_data[(filtered_data['Amount'] >= min_amount) & (filtered_data['Amount'] <= max_amount)]
year_2020_data = filtered_data[filtered_data['Year_Funded'] == 2020]
sector_funding_2020 = year_2020_data.groupby('Industry')['Amount'].sum().reset_index()
fig = px.bar(sector_funding_2020, x='Industry', y='Amount')
fig.update_xaxes(categoryorder='total descending')  # Sort sectors by total funding amount in descending order
fig.update_traces(marker_color='blue')  
st.plotly_chart(fig)
sector_counts = filtered_data['Industry'].value_counts().reset_index()
sector_counts.columns = ['Industry', 'Startup Count']
# Create a bar chart for the number of startups by industry
st.subheader("Number of Startups by Industry")
fig2 = px.bar(sector_counts, x='Industry', y='Startup Count')
st.plotly_chart(fig2)


st.subheader("Startup Counts by Sector") 
fig = px.bar(sector_counts, x='Industry', y='Startup Count')
fig.update_xaxes(categoryorder='total descending')  # Sort sectors by the count of startups in descending order
# Customize the chart if needed
fig.update_traces(marker_color='green')  # You can change the bar color
# Display the chart in your Streamlit app
st.plotly_chart(fig)


industry_name = 'EV'
industry_data = data[data['Industry'] == industry_name]
 
funding_by_year = industry_data.groupby('Year_Funded')['Amount'].sum().reset_index()
 
fig = px.line(funding_by_year, x='Year_Funded', y='Amount', title=f'Funding Evolution for EVs Over Time')
fig.update_xaxes(type='category')
fig.update_traces(mode='lines+markers')
 
st.plotly_chart(fig)


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






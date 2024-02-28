import streamlit as st
import pandas as pd
import plotly.express as px
from random import sample
from APIcall import get_chat_completions
from collections import defaultdict

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('myverbs.csv')

data = load_data()

tab1, tab2 = st.tabs(["Recommend", "Summary"])

# Sidebar filters
st.sidebar.title("Filters")

# Radio button to select between Total and Filtered
filter_type = st.sidebar.radio("Select view:", ["Total", "Filtered"])


if filter_type == "Filtered":
        # Obtain unique values for age and brand
        all_age_groups = data['Age'].unique()
        all_brands = data['Brand'].unique()

        # Define filter variables with all options selected by default
        age_filter = st.sidebar.multiselect("Select Age:", all_age_groups, all_age_groups)
        brand_filter = st.sidebar.multiselect("Select Brand:", all_brands, all_brands)

        # Apply filters
        filtered_data = data[(data['Age'].isin(age_filter)) & (data['Brand'].isin(brand_filter))]

        # Calculate topic percentages using filtered data
        topics = filtered_data.columns[1:13]
        topic_percentages = {}
        topic_samples = {}
        for topic in topics:
            topic_percentages[topic] = round((filtered_data[topic] == '✓').sum() / len(filtered_data) * 100, 4)
            positive_indices = filtered_data.index[filtered_data[topic] == '✓'].tolist()
            sample_size = min(3, len(positive_indices))
            topic_samples[topic] = sample(filtered_data.loc[positive_indices, 'text'].tolist(), sample_size)

        # Create a chart for topic percentages using filtered data
        st.write("## Topic Percentages")
        fig = px.bar(x=list(topic_percentages.keys()), y=list(topic_percentages.values()), labels={'x':'Topics', 'y':'Percentage'})
        fig.update_layout(xaxis={'categoryorder':'total descending'}, yaxis_title="Percentage")

        # Construct custom hovertemplate with verbatim for each topic
        hovertemplate = []
        for topic, samples in topic_samples.items():
            tooltip_text = f"<b>{topic}</b><br><br>Percentage: {topic_percentages[topic]}%<br><br>Sample Verbatim:<br>"
            tooltip_text += "<br>".join([f"- {sample_text}" for sample_text in samples])
            hovertemplate.append(tooltip_text)

        # Update hovertemplate for each bar in the chart
        fig.update_traces(hovertemplate=hovertemplate)

        # Write a short heading
        heading = get_chat_completions(f"Summarise the top topics in two sentences, in the format X, Y, and Z are the top 5 cited themes, accounting for x% of the total mentions(no decimals). Here's the data {topic_percentages}. Don't comment on the 'Other' mentions.")
        st.write(heading)

        # Display the chart in the main area
        st.plotly_chart(fig)

        # Display the filtered dataset in a separate tab in the sidebar
        st.write("## Filtered Dataset")
        st.write(filtered_data)

        # Add a download button for the filtered dataset
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='filtered_myverbs.csv',
            mime='text/csv'
        )
else:
        # Calculate topic percentages for total dataset
        topics = data.columns[1:13]
        topic_percentages = {}
        topic_samples = {}
        for topic in topics:
            topic_percentages[topic] = round((data[topic] == '✓').sum() / len(data) * 100, 4)
            positive_indices = data.index[data[topic] == '✓'].tolist()
            sample_size = min(3, len(positive_indices))
            topic_samples[topic] = sample(data.loc[positive_indices, 'text'].tolist(), sample_size)

        # Create a chart for topic percentages for total dataset
        st.write("## Topic Percentages (Total)")
        fig = px.bar(x=list(topic_percentages.keys()), y=list(topic_percentages.values()), labels={'x':'Topics', 'y':'Percentage'})
        fig.update_layout(xaxis={'categoryorder':'total descending'}, yaxis_title="Percentage")

        # Construct custom hovertemplate with verbatim for each topic for total dataset
        hovertemplate = []
        for topic, samples in topic_samples.items():
            tooltip_text = f"<b>{topic}</b><br><br>Percentage: {topic_percentages[topic]}%<br><br>Sample Verbatim:<br>"
            tooltip_text += "<br>".join([f"- {sample_text}" for sample_text in samples])
            hovertemplate.append(tooltip_text)

        # Update hovertemplate for each bar in the chart for total dataset
        fig.update_traces(hovertemplate=hovertemplate)

        # Write a short heading
        heading = get_chat_completions(f"Summarise the top topics in two sentences, in the format X, Y, and Z are the top 5 cited themes, accounting for x% of the total mentions (no decimals). Here's the data {topic_percentages}. Don't comment on the other mentions.")
        st.write(heading)

        # Display the chart for total dataset in the main area
        st.plotly_chart(fig)

        # Display the total dataset in a separate tab in the sidebar
        st.write("## Total Dataset")
        st.write(data)

        # Add a download button for the total dataset
        csv = data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='myverbs.csv',
            mime='text/csv'
        )

with tab2:
    st.write("## Summary by Age Group")



    # Grouping data by age
    age_groups = data.groupby('Age')

    # Initialize dictionaries to store results for each age group
    age_group_topic_percentages = defaultdict(dict)
    age_group_topic_samples = defaultdict(dict)

    for age, age_group_data in age_groups:
        # Filtering data for the current age group
        filtered_data = age_group_data
        
        # Perform the analysis for each topic
        for topic in topics:
            topic_percentages = round((filtered_data[topic] == '✓').sum() / len(filtered_data) * 100, 4)
            positive_indices = filtered_data.index[filtered_data[topic] == '✓'].tolist()
            sample_size = min(3, len(positive_indices))
            topic_samples = sample(filtered_data.loc[positive_indices, 'text'].tolist(), sample_size)
            
            # Storing results for each topic in the current age group
            age_group_topic_percentages[age][topic] = topic_percentages
            age_group_topic_samples[age][topic] = topic_samples

    
   # age_summary = get_chat_completions(f"Summarise any intereseting differences by age within two paragraphs, focusing on the percentages of the total mentions (no decimals). Here's the data {age_group_topic_percentages}. Don't comment on the other mentions.")
    
    
    @st.cache_data()
    def get_age_summary(prompt):
        summary = get_chat_completions(prompt)
        return summary
    
    age_summary = get_age_summary(f"Summarise any intereseting differences by age within two paragraphs, focusing on the percentages of the total mentions (no decimals). Here's the data {age_group_topic_percentages}. Don't comment on the other mentions.")
    
    st.write(age_summary)

    st.write("## Summary by Brand")

    # Grouping data by brand
    brand_groups = data.groupby('Brand')

    # Initialize dictionaries to store results for each brand group
    brand_group_topic_percentages = defaultdict(dict)
    brand_group_topic_samples = defaultdict(dict)

    for brand, brand_group_data in brand_groups:
        # Filtering data for the current brand group
        filtered_data = brand_group_data
        
        # Perform the analysis for each topic
        for topic in topics:
            topic_percentages = round((filtered_data[topic] == '✓').sum() / len(filtered_data) * 100, 4)
            positive_indices = filtered_data.index[filtered_data[topic] == '✓'].tolist()
            sample_size = min(3, len(positive_indices))
            topic_samples = sample(filtered_data.loc[positive_indices, 'text'].tolist(), sample_size)
            
            # Storing results for each topic in the current brand group
            brand_group_topic_percentages[brand][topic] = topic_percentages
            brand_group_topic_samples[brand][topic] = topic_samples

    # Create a summary for brand groups
   # brand_summary = get_chat_completions(f"Summarise any intereseting differences by brand within two paragraphs, focusing on percentages of the total mentions (no decimals). Here's the data {brand_group_topic_percentages}. Don't comment on the other mentions.")
    
    @st.cache_data()
    def get_brand_summary(prompt):
        summary = get_chat_completions(prompt)
        return summary
    
    
    brand_summary = get_brand_summary(f"Summarise any intereseting differences by brand within two paragraphs, focusing on percentages of the total mentions (no decimals). Here's the data {brand_group_topic_percentages}. Don't comment on the other mentions.")    
    st.write(brand_summary)

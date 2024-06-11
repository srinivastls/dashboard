import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load and process data from the uploaded Excel file
def load_data(file):
    data = pd.read_excel(file, parse_dates=['Created', 'Due date', 'Updated'])
    data = data.drop_duplicates(subset='Issue key')
    return data

# Function to add "Select All" functionality to multiselect
def multiselect_with_select_all(label, options, key):
    select_all = st.checkbox(f"Select all {label}", key=key+'_select_all')
    if select_all:
        selected_options = st.multiselect(label, options, default=options, key=key)
    else:
        selected_options = st.multiselect(label, options, key=key)
    return selected_options

# Title and description
st.title("Jira Dashboard")
st.write("Upload an Excel file containing Jira data to view the dashboard.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    daat = load_data(uploaded_file)
else:
    st.write("Please upload an Excel file to proceed.")
    st.stop()

# Display the raw data
st.subheader("Raw Data")
st.dataframe(daat)

# Filter options with "Select All" option in dropdown
st.subheader("Filter Data")
status_filter = multiselect_with_select_all("Status", daat['Status'].unique(), 'status')
assignee_filter = multiselect_with_select_all("Assignee", daat['Assignee'].unique(), 'assignee')
issue_type_filter = multiselect_with_select_all("Issue Type", daat['Issue Type'].unique(), 'issue_type')
priority_filter = multiselect_with_select_all("Priority", daat['Priority'].unique(), 'priority')

filtered_data = daat[
    (daat['Status'].isin(status_filter)) &
    (daat['Assignee'].isin(assignee_filter)) &
    (daat['Issue Type'].isin(issue_type_filter)) &
    (daat['Priority'].isin(priority_filter))
]

st.dataframe(filtered_data)

# KPIs
st.subheader("Key Performance Indicators (KPIs)")
total_issues = len(daat)
total_filtered_issues = len(filtered_data)
issues_by_status = daat['Status'].value_counts()
average_resolution_time = (daat['Updated'] - daat['Created']).dt.days.mean()

st.metric("Total Issues", total_issues)
st.metric("Total Issues (Filtered)", total_filtered_issues)
st.metric("Average Resolution Time (days)", f"{average_resolution_time:.2f}" if not pd.isna(average_resolution_time) else 'N/A')



# Calculate and display average resolution time for individual assignees
st.subheader("Average Resolution Time by Assignee")
if 'Assignee' in filtered_data.columns and 'Created' in filtered_data.columns and 'Updated' in filtered_data.columns:
    filtered_data['Resolution Time (days)'] = (filtered_data['Updated'] - filtered_data['Created']).dt.days
    avg_resolution_time_by_assignee = filtered_data.groupby('Assignee')['Resolution Time (days)'].mean().reset_index()
    
# Visualizations
st.subheader("Visualizations")

# Helper function to annotate bar charts
def annotate_bar_chart(fig):
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    return fig


fig = px.pie(filtered_data, names='Status', title='Issues by Status', hole=0.3)
st.plotly_chart(fig)

assignee_counts = filtered_data['Assignee'].value_counts().reset_index()
assignee_counts.columns = ['Assignee', 'Count']
fig = px.bar(assignee_counts, x='Assignee', y='Count', title='Issues by Assignee')
fig = annotate_bar_chart(fig)
st.plotly_chart(fig)


fig = px.pie(filtered_data, names='Priority', title='Issues by Priority', hole=0.3)
st.plotly_chart(fig)

issue_type_counts = filtered_data['Issue Type'].value_counts().reset_index()
issue_type_counts.columns = ['Issue Type', 'Count']
fig = px.bar(issue_type_counts, x='Issue Type', y='Count', title='Issues by Issue Type')
fig = annotate_bar_chart(fig)
st.plotly_chart(fig)


if 'Resolution Time (days)' in filtered_data.columns:
    fig = px.bar(avg_resolution_time_by_assignee, x='Assignee', y='Resolution Time (days)', 
                 title='Average Resolution Time by Assignee')
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    st.plotly_chart(fig)


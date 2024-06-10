import streamlit as st
import pandas as pd
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    data = data.drop_duplicates(subset='Issue key')

    # Title and description
    st.title("Dashboard")
    st.write("This dashboard displays data from an Excel file.")

    # Display the raw data
    st.subheader("Raw Data")
    st.dataframe(data)

    # Filter options
    st.subheader("Filter Data")
    status_filter = st.multiselect("Select Status", options=data['Status'].unique(), default=data['Status'].unique())
    assignee_filter = st.multiselect("Select Assignee", options=data['Assignee'].unique(), default=data['Assignee'].unique())
    task_filter = st.multiselect("Select Task", options=data['Issue Type'].unique(), default=data['Issue Type'].unique())
    #priority_filter = st.multiselect("Select Priority", options=data['Priority'].unique(), default=data['Priority'].unique())

    filtered_data = data[
        (data['Status'].isin(status_filter)) &
        (data['Assignee'].isin(assignee_filter)) &
        (data['Issue Type'].isin(task_filter)) 
        #(data['Priority'].isin(priority_filter))
    ]

    st.dataframe(filtered_data)

    # Metrics
    st.subheader("Metrics")
    st.write("Total Issues:", len(data))
    st.write("Total Issues (Filtered):", len(filtered_data))

    # Visualizations
    st.subheader("Visualizations")

    # Pie chart of issues by status
    status_counts = filtered_data['Status'].value_counts()
    st.write("Issues by Status")
    st.bar_chart(status_counts)

    # Bar chart of issues by assignee
    assignee_counts = filtered_data['Assignee'].value_counts()
    st.write("Issues by Assignee")
    st.bar_chart(assignee_counts)

    # Pie chart of issues by priority
    #priority_counts = filtered_data['Priority'].value_counts()
    #st.write("Issues by Priority")
    #st.line_chart(priority_counts)

    # Bar chart of issues by task
    task_counts = filtered_data['Issue Type'].value_counts()
    st.write("Issues by Task")
    st.bar_chart(task_counts)
else:
    st.write("Please upload an Excel file to proceed.")
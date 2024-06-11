import streamlit as st
import pandas as pd
uploaded_file = st.file_uploader("Choose an Excel file", type="csv")
use_default = st.button("Use Default Data")

if uploaded_file is not None:
    # Load the data from the uploaded file
    data = pd.read_csv(uploaded_file)
    data = data.drop_duplicates(subset='Issue key')
elif use_default:
    # Load the default data
    data = pd.read_csv("data.csv")
    data = data.drop_duplicates(subset='Issue key')
    st.write("Using default data from default_data.csv")
else:
    st.write("Please upload an Excel file or use the default data to proceed.")
    st.stop()

st.title("Dashboard")
st.write("This dashboard displays data from an Excel file.")

st.subheader("Raw Data")
st.dataframe(data)

st.subheader("Filter Data")
status_filter = st.multiselect("Select Status", options=data['Status'].unique(), default=data['Status'].unique())
assignee_filter = st.multiselect("Select Assignee", options=data['Assignee'].unique(), default=data['Assignee'].unique())
task_filter = st.multiselect("Select Task", options=data['Issue Type'].unique(), default=data['Issue Type'].unique())

filtered_data = data[
    (data['Status'].isin(status_filter)) &
    (data['Assignee'].isin(assignee_filter)) &
    (data['Issue Type'].isin(task_filter)) 
        ]

st.dataframe(filtered_data)

st.subheader("Metrics")
st.write("Total Issues:", len(data))
st.write("Total Issues (Filtered):", len(filtered_data))

st.subheader("Visualizations")

status_counts = filtered_data['Status'].value_counts()
st.write("Issues by Status")
st.bar_chart(status_counts)

assignee_counts = filtered_data['Assignee'].value_counts()
st.write("Issues by Assignee")
st.bar_chart(assignee_counts)

task_counts = filtered_data['Issue Type'].value_counts()
st.write("Issues by Task")
st.bar_chart(task_counts)

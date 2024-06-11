import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

uploaded_file = st.file_uploader("Choose an Excel file", type="csv")


def multiselect_with_select_all(label, options, key):
    select_all = st.checkbox(f"Select all {label}", key=key+'_select_all')
    if select_all:
        selected_options = st.multiselect(label, options, default=options, key=key)
    else:
        selected_options = st.multiselect(label, options, key=key)
    return selected_options

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data = data.drop_duplicates(subset='Issue key')

    st.title("Dashboard")
    st.write("This dashboard displays data from an Excel file.")

    st.subheader("Raw Data")
    st.dataframe(data)

    st.subheader("Filter Data")
    status_filter = multiselect_with_select_all("Status", data['Status'].unique(), data['Status'].unique())
    assignee_filter = multiselect_with_select_all("Assignee", data['Assignee'].unique(), data['Assignee'].unique())
    task_filter = multiselect_with_select_all("Issue Type", data['Issue Type'].unique(), data['Issue Type'].unique())


    filtered_data = data[
        (data['Status'].isin(status_filter)) &
        (data['Assignee'].isin(assignee_filter)) &
        (data['Issue Type'].isin(task_filter)) 
         ]

    st.dataframe(filtered_data)
    st.subheader("Key Performance Indicators (KPIs)")

    st.subheader("Average Resolution Time by Assignee")
    if 'Assignee' in filtered_data.columns and 'Created' in filtered_data.columns and 'Updated' in filtered_data.columns:
        filtered_data['Created1'] = pd.to_datetime(filtered_data['Created'])
        filtered_data['Updated1'] = pd.to_datetime(filtered_data['Updated'])
        filtered_data['Resolution Time (days)'] = (filtered_data['Updated1'] - filtered_data['Created1']).dt.days
        st.dataframe(filtered_data)
        avg_resolution_time_by_assignee = filtered_data.groupby('Assignee')['Resolution Time (days)'].mean().reset_index()
        for index, row in avg_resolution_time_by_assignee.iterrows():
            st.metric(f"Avg Resolution Time for {row['Assignee']}", f"{row['Resolution Time (days)']:.2f} days")

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
    # Bar chart of issues by assignee using Plotly
    st.write("Issues by Assignee")
    assignee_counts = filtered_data['Assignee'].value_counts().reset_index()
    assignee_counts.columns = ['Assignee', 'Count']
    fig = px.bar(assignee_counts, x='Assignee', y='Count', title='Issues by Assignee')
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig)

    # Pie chart of issues by priority using Plotly
    st.write("Issues by Priority")
    fig = px.pie(filtered_data, names='Priority', title='Issues by Priority', hole=0.3)
    st.plotly_chart(fig)

    # Bar chart of issues by issue type using Plotly
    st.write("Issues by Issue Type")
    issue_type_counts = filtered_data['Issue Type'].value_counts().reset_index()
    issue_type_counts.columns = ['Issue Type', 'Count']
    fig = px.bar(issue_type_counts, x='Issue Type', y='Count', title='Issues by Issue Type')
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig)

    # Bar chart of average resolution time by assignee using Plotly
    st.write("Average Resolution Time by Assignee")
    if 'Resolution Time (days)' in filtered_data.columns:
        fig = px.bar(avg_resolution_time_by_assignee, x='Assignee', y='Resolution Time (days)', 
                    title='Average Resolution Time by Assignee')
        fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        st.plotly_chart(fig)


else:
    st.write("Please upload an Excel file to proceed.")
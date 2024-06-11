import streamlit as st
import pandas as pd
import plotly.express as px

def upload_file():
    data = None
    uploaded_file = st.sidebar.file_uploader("Upload a file", type=['csv', 'xlsx', 'json', 'txt'])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension == 'csv':
            data = pd.read_csv(uploaded_file, parse_dates=['Created', 'Due date', 'Updated'])
        elif file_extension == 'xlsx':
            data = pd.read_excel(uploaded_file, parse_dates=['Created', 'Due date', 'Updated'])
        elif file_extension == 'json':
            data = pd.read_json(uploaded_file, parse_dates=['Created', 'Due date', 'Updated'])
        elif file_extension == 'txt':
            data = pd.read_csv(uploaded_file, sep='\t', parse_dates=['Created', 'Due date', 'Updated'])
        data = data.drop_duplicates(subset='Issue key')
    return data

def multiselect_with_select_all(label, options, key):
    select_all = st.sidebar.checkbox(f"Select all {label}", key=key+'_select_all', value=True)
    if select_all:
        selected_options = st.sidebar.multiselect(label, options, default=options, key=key)
    else:
        selected_options = st.sidebar.multiselect(label, options, key=key)
    return selected_options



st.title("Dashboard")
uploaded_file = upload_file()

if uploaded_file is not None:
    data = uploaded_file
else:
    st.write("Please upload a  data file to proceed.")
    st.stop()

st.sidebar.subheader("Filter Data")
status_filter = multiselect_with_select_all("Status", data['Status'].unique(), 'status')
assignee_filter = multiselect_with_select_all("Assignee", data['Assignee'].unique(), 'assignee')
issue_type_filter = multiselect_with_select_all("Issue Type", data['Issue Type'].unique(), 'issue_type')
priority_filter = multiselect_with_select_all("Priority", data['Priority'].unique(), 'priority')

filtered_data = data[
    (data['Status'].isin(status_filter)) &
    (data['Assignee'].isin(assignee_filter)) &
    (data['Issue Type'].isin(issue_type_filter)) &
    (data['Priority'].isin(priority_filter))
]

st.subheader("Raw Data")
st.dataframe(data)

st.subheader("Filtered Data")
st.dataframe(filtered_data)

st.subheader("Data Stats")
total_issues = len(data)
total_filtered_issues = len(filtered_data)

st.metric("Total Issues", total_issues)
st.metric("Total Issues (Filtered)", total_filtered_issues)

if 'Assignee' in filtered_data.columns and 'Created' in filtered_data.columns and 'Updated' in filtered_data.columns:
    filtered_data['Resolution Time (days)'] = (filtered_data['Updated'] - filtered_data['Created']).dt.days
    avg_resolution_time_by_assignee = filtered_data.groupby('Assignee')['Resolution Time (days)'].mean().reset_index()

if len(status_filter) > 0 and len(assignee_filter) > 0 and len(issue_type_filter) > 0 and len(priority_filter) > 0:
    st.subheader("Visualizations")

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
    if 'Resolution Time (days)' in filtered_data.columns:
        fig = px.bar(avg_resolution_time_by_assignee, x='Assignee', y='Resolution Time (days)', 
                        title='Average Resolution Time by Assignee')
        fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        st.plotly_chart(fig)
    issue_type_counts = filtered_data['Issue Type'].value_counts().reset_index()
    issue_type_counts.columns = ['Issue Type', 'Count']
    fig = px.bar(issue_type_counts, x='Issue Type', y='Count', title='Issues by Issue Type')
    fig = annotate_bar_chart(fig)
    st.plotly_chart(fig)


st.subheader("Task Completion Status")
# Calculate completion status
filtered_data['Completion Status'] = None
filtered_data.loc[filtered_data['Due date'].notnull(), 'Completion Status'] = \
    filtered_data['Due date'].lt(filtered_data['Updated']).map({True: 'After Deadline', False: 'Before Deadline'})
filtered_data.loc[filtered_data['Due date'].isnull(), 'Completion Status'] = 'No Deadline'

completion_status_counts = filtered_data['Completion Status'].value_counts()
st.write(completion_status_counts)



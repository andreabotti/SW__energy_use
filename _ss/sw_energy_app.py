import pandas as pd, numpy as np
import plotly.express as px
from datetime import datetime
import streamlit as st
from streamlit_super_slider import st_slider


def process_data(df):
    # Exclude non-time columns for melting
    time_columns = df.columns.drop(['Account Number', 'MPAN', 'Meter Serial Number', 'Date'])
    df_corrected_melted = df.melt(id_vars=["Date"], value_vars=time_columns, var_name="Time", value_name="Energy")

    # Combine Date and Time columns to create a datetime index
    df_corrected_melted['Datetime'] = pd.to_datetime(df_corrected_melted['Date'] + ' ' + df_corrected_melted['Time'], dayfirst=True)

    # Set the new datetime index
    df_corrected_melted = df_corrected_melted.set_index('Datetime')

    # Dropping the original Date and Time columns
    df_corrected_melted.drop(columns=['Date', 'Time'], inplace=True)

    # Resample the data to hourly resolution and sum the energy values
    df_hourly = df_corrected_melted.resample('H').sum()

    # Create daily and monthly dataframes by summing up the hourly data
    df_daily = df_hourly.resample('D').sum()
    df_monthly = df_hourly.resample('M').sum()

    return df_hourly, df_daily, df_monthly




def prepare__df_hourly_heatmap(df):
    df_hourly_heatmap = df.reset_index()
    df_hourly_heatmap['Date'] = df_hourly_heatmap['Datetime'].dt.strftime('%Y-%m-%d')
    df_hourly_heatmap['Hour'] = df_hourly_heatmap['Datetime'].dt.hour
    return df_hourly_heatmap


def create__fig_hourly_heatmap(df, label_hrs):
    mon = df['Datetime'].iloc[0].strftime("%b")
    fig_hourly_heatmap = px.density_heatmap(
        df, x='Date', y='Hour', z='Energy', 
        title=f'Hourly Heatmap for {mon}', 
        color_continuous_scale='hot_r',
        range_color=[0, 40],
        # category_orders={'Hour': label_hrs},
        nbinsy=24
        )
    fig_hourly_heatmap.update_layout(
        height=350,
        title_x=0.5,
        margin=dict(l=0, r=0, t=30, b=0),
        )
    fig_hourly_heatmap.update_layout(
        xaxis={'type': 'category'},
        title={
            'x': 0.5,
            'xanchor': 'center',
            # 'yanchor': 'top',
            }
        )
    fig_hourly_heatmap.update_layout(coloraxis_showscale=False)

    fig_hourly_heatmap.update_xaxes(title_text='Date')

    hour_labels = np.arange(0, 24, 3)
    fig_hourly_heatmap.update_yaxes(
        title_text='Hour of the Day',
        tickmode='array',
        tickvals=hour_labels,
        ticktext=hour_labels.astype(str)  # Convert to string for display
        )

    return fig_hourly_heatmap



# Plot using Plotly
def create__typ_day__line_chart(df):

    fig = px.line(df, x='Hour', y='Average Energy', markers=True, title=f'Typical Day Profile for {mon}')
    fig.update_layout(xaxis_title='Hour of Day', yaxis_title='Average Energy')

    fig.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=30, b=0),
        yaxis=dict(range=[0, 21]),
        )
    fig.update_layout(
        xaxis={'type': 'category'},
        title={
            'x': 0.5,
            'xanchor': 'center',
            }
        )

    return fig




# Streamlit app configuration for wide mode
st.set_page_config(layout="wide")

# Streamlit app starts here
st.title('Electricity Consumption Data Processor')


# File uploader widget
uploaded_file = st.sidebar.file_uploader('Upload a CSV file', type='csv')

st.sidebar.markdown('---')
# Sidebar for user choices
choice = st.sidebar.selectbox("Choose Data View", ["All Year Data", "Monthly Data"])





if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Process the data
    df_hourly, df_daily, df_monthly = process_data(df)


    if choice == "All Year Data":
        # Plotly line chart for df_hourly
        fig_hourly_line = px.line(df_hourly.reset_index(), x='Datetime', y='Energy', title='Hourly Electricity Consumption')
        fig_hourly_line.update_xaxes(rangeslider_visible=True)
        fig_hourly_line.update_yaxes(title_text='Energy (kWh)')
        st.plotly_chart(fig_hourly_line, use_container_width=True)

        # Plotly column chart for df_daily
        fig_daily = px.bar(df_daily.reset_index(), x='Datetime', y='Energy', title='Daily Electricity Consumption')
        fig_daily.update_yaxes(title_text='Energy (kWh)')
        st.plotly_chart(fig_daily, use_container_width=True)

        # Plotly column chart for df_monthly
        fig_monthly = px.bar(df_monthly.reset_index(), x='Datetime', y='Energy', title='Monthly Electricity Consumption')
        fig_monthly.update_yaxes(title_text='Energy (kWh)')
        st.plotly_chart(fig_monthly, use_container_width=True)



    elif choice == "Monthly Data":


        st.markdown('---')
        
        month_options = pd.Series(range(2,12))

        selected_month = st.select_slider("Select Month", options=month_options, format_func=lambda x: datetime(1900, x, 1).strftime('%B'))

        # Use the Streamlit Super Slider component
        # selected_month = st_slider(values=month_options)

    
        # Filter data for selected month
        df_hourly_month = df_hourly[df_hourly.index.month == selected_month]


        # Example: Creating a dictionary of dummy dataframes
        df_dict = {}
        for i in range(1,13):
            df_hourly_month = df_hourly[df_hourly.index.month == i]
            df_dict[i] = df_hourly_month


        df_dict__typ_day = {}
        for i in range(1,13):
            df_hourly_month = df_hourly[df_hourly.index.month == i]

            df_hourly_month['Hour'] = df_hourly_month.index.hour
            typical_day = df_hourly_month.groupby('Hour')['Energy'].mean()

            # Create a DataFrame for plotting (if needed)
            typical_day_df = pd.DataFrame({'Hour': typical_day.index, 'Average Energy': typical_day.values})
            df_dict__typ_day[i] = typical_day_df




        # Ensure all hours of the day are represented
        all_hours = np.arange(24)
        no_hrs = all_hours

        col1, spacing, col2, spacing, col3 = st.columns([10,1,10,1,10])

        with col1:
            df_table = df_dict[1]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[1]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

            st.markdown('---')

        with col2:
            df_table = df_dict[2]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[2]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

            st.markdown('---')

        with col3:
            df_table = df_dict[3]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[3]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

            st.markdown('---')


        with col1:
            df_table = df_dict[4]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[4]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

        with col2:
            df_table = df_dict[5]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[5]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

        with col3:
            df_table = df_dict[6]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[6]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)


        st.markdown('---')


        with col1:
            df_table = df_dict[7]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[7]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

        with col2:
            df_table = df_dict[8]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[8]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

        with col3:
            df_table = df_dict[9]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[9]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)


        st.markdown('---')


        with col1:
            df_table = df_dict[10]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[10]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

        with col2:
            df_table = df_dict[11]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[11]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

        with col3:
            df_table = df_dict[12]
            mon = df_table.index[0].strftime("%b")

            df_plot = prepare__df_hourly_heatmap(df_table)
            fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
            st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

            df_table_typday = df_dict__typ_day[12]
            fig_hourly_typday = create__typ_day__line_chart(df_table_typday)
            st.plotly_chart(fig_hourly_typday, use_container_width=True)

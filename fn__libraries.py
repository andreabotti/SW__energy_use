import pandas as pd, numpy as np
import plotly.express as px
from datetime import datetime
from datetime import timedelta
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
def create__typ_day__line_chart(df, month):

    fig = px.line(df, x='Hour', y='Average Energy', markers=True, title=f'Typical Day Profile for {month}')
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



# Function to add weekend highlights
def add_weekend_highlights(fig, weekends):
    
    # Add grey bands for weekends
    for date in weekends:
        fig.add_vrect(
            x0=date, x1=date + timedelta(days=1),
            fillcolor='grey', opacity=0.2,
            layer='below', line_width=0
        )


def add_weekend_highlights_group(fig, df):
    # Find continuous weekend periods
    df['Weekend'] = df.index.weekday >= 5
    df['Weekend_Group'] = (df['Weekend'] != df['Weekend'].shift()).cumsum()
    
    for _, group in df[df['Weekend']].groupby('Weekend_Group'):
        start, end = group.index.min(), group.index.max() + pd.Timedelta(days=1)
        fig.add_vrect(
            x0=start, x1=end,
            fillcolor='grey', opacity=0.2,
            layer='below', line_width=0
        )
# IMPORT LIBRARIES
# from fn__import_py_libs import *
from fn__libraries import *
mapbox_access_token = 'pk.eyJ1IjoiYW5kcmVhYm90dGkiLCJhIjoiY2xuNDdybms2MHBvMjJqbm95aDdlZ2owcyJ9.-fs8J1enU5kC3L4mAJ5ToQ'





# PAGE CONFIG
st.set_page_config(page_title="SW Energy Data",   page_icon=':mostly_sunny:', layout="wide")
st.markdown(
    """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 2.5rem; padding-right: 2.5rem;}</style>""",
    unsafe_allow_html=True)




# TOP CONTAINER
top_col1, top_col2 = st.columns([6,1])
with top_col1:
    st.markdown("# Stanton Williams Energy 2023")
    st.markdown("#### Reporting of Stanton Williams metered electricity data from 2023")
    st.caption('Developed by AB.S.RD - https://absrd.xyz/')
st.markdown('---')
##### ##### ##### ##### ##### ##### ##### #####




##### ##### ##### ##### ##### ##### ##### #####
df_hourly   = st.session_state['df_hourly']
df_daily    = st.session_state['df_daily']
df_monthly  = st.session_state['df_monthly']




##### ##### ##### ##### ##### ##### ##### #####
# Checklist to toggle weekend highlights
st.sidebar.markdown('### Chart settings')
marker_color = st.sidebar.color_picker(
    'Marker colour',
    value='#0099cc',
    help=None, on_change=None,
    )
opacity = 0.4
hex = marker_color.lstrip('#')
marker_color__rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
marker_color__rgba = 'rgba' + str(marker_color__rgb + (opacity,))
st.sidebar.write(f'RGB: {marker_color__rgb} | HEX: {marker_color}')

# st.sidebar.divider()
show_weekends = st.sidebar.checkbox('Highlight weekends')



##### ##### ##### ##### ##### ##### ##### #####
tab_hourly, tab_daily, tab_monthly = st.tabs(['Hourly Frequency', 'Daily Frequency', 'Monthly Frequency'])


with tab_hourly:

    # Reset index if 'Datetime' is not already a column
    df_plot = df_hourly.reset_index()

    # Create a scatter plot (line chart) using go.Scatter
    fig_hourly_line = go.Figure()
    fig_hourly_line.add_trace(
        go.Scatter(
            x=df_plot['Datetime'],
            y=df_plot['Energy'],
            mode='lines',
            fill='tozeroy',
            fillcolor=marker_color__rgba,
            line_color=marker_color,
            )
    )
    fig_hourly_line.update_layout(
        title='Hourly Electricity Consumption',
        xaxis_title='Datetime',
        yaxis_title='Energy (kWh)',
    )
    fig_hourly_line.update_xaxes(rangeslider_visible=True)
    fig_hourly_line.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    # dict(count=3,label="3d",step="day",stepmode="backward"),
                    dict(count=7,label="7d",step="day",stepmode="backward"),
                    dict(count=14,label="14d",step="day",stepmode="backward"),
                    dict(count=1,label="1m",step="month",stepmode="backward"),
                    dict(count=3,label="3m",step="month",stepmode="backward"),
                    dict(step="all"),
                ])
            ),
        rangeslider=dict(visible=True),
        type="date"
        )
    )

    if show_weekends:
        add_weekend_highlights_group(fig=fig_hourly_line, df=df_hourly)

    st.plotly_chart(fig_hourly_line, use_container_width=True)



with tab_daily:
    # Plotly column chart for df_daily
    df_plot = df_daily.reset_index()
    fig_daily_bar = go.Figure()
    # fig_daily_bar = px.bar(df_daily.reset_index(), x='Datetime', y='Energy', title='Daily Electricity Consumption')
    fig_daily_bar.add_trace(
        go.Bar(
            x=df_plot['Datetime'], y=df_plot['Energy'], marker_color=marker_color,
            )
    )
    fig_daily_bar.update_layout(
        title='Daily Electricity Consumption',
        xaxis_title='Datetime',
        yaxis_title='Energy (kWh)'
    )
    fig_daily_bar.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    # dict(count=3,label="3d",step="day",stepmode="backward"),
                    dict(count=7,label="7d",step="day",stepmode="backward"),
                    dict(count=14,label="14d",step="day",stepmode="backward"),
                    dict(count=1,label="1m",step="month",stepmode="backward"),
                    dict(count=3,label="3m",step="month",stepmode="backward"),
                    dict(step="all"),
                ])
            ),
        rangeslider=dict(visible=True),
        type="date"
        )
    )

    if show_weekends:
        add_weekend_highlights_group(fig=fig_daily_bar, df=df_daily)

    st.plotly_chart(fig_daily_bar, use_container_width=True)



with tab_monthly:

    # Plotly column chart for df_monthly
    fig_monthly = px.bar(df_monthly.reset_index(), x='Datetime', y='Energy', title='Monthly Electricity Consumption')

    fig_monthly.update_traces(marker_color=marker_color__rgb)
    fig_monthly.update_yaxes(title_text='Energy (kWh)')
    st.plotly_chart(fig_monthly, use_container_width=True)

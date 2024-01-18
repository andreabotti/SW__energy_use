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
show_weekends = st.sidebar.checkbox('Highlight Weekends')



##### ##### ##### ##### ##### ##### ##### #####
tab_hourly, tab_daily, tab_monthly = st.tabs(['Hourly Frequency', 'Daily Frequency', 'Monthly Frequency'])


with tab_hourly:
    # Plotly line chart for df_hourly
    fig_hourly_line = px.line(df_hourly.reset_index(), x='Datetime', y='Energy', title='Hourly Electricity Consumption')
    fig_hourly_line.update_xaxes(rangeslider_visible=True)
    fig_hourly_line.update_yaxes(title_text='Energy (kWh)')
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
    fig_daily_bar = px.bar(df_daily.reset_index(), x='Datetime', y='Energy', title='Daily Electricity Consumption')
    fig_daily_bar.update_yaxes(title_text='Energy (kWh)')
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
    fig_monthly.update_yaxes(title_text='Energy (kWh)')
    st.plotly_chart(fig_monthly, use_container_width=True)

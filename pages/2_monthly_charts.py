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
top_col1, top_col2 = st.columns([3,1])
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
# show_weekends = st.sidebar.checkbox('Highlight Weekends')




month_options = pd.Series(range(2,12))

# Use the Streamlit Super Slider component
# selected_month = st.select_slider("Select Month", options=month_options, format_func=lambda x: datetime(1900, x, 1).strftime('%B'))
# selected_month = st_slider(values=month_options)
# df_hourly_month = df_hourly[df_hourly.index.month == selected_month]



##### ##### ##### ##### ##### ##### ##### #####
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



winter1_tab, spring_tab, summer_tab, autumn_tab = st.tabs(['Q1 2023','Q2 2023','Q3 2023','Q4 2023'])

with winter1_tab:
    col1, spacing, col2, spacing, col3 = st.columns([10,1,10,1,10])

    with col1:
        df_table = df_dict[1]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[1]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)


    with col2:
        df_table = df_dict[2]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[2]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)


    with col3:
        df_table = df_dict[3]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[3]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)




with spring_tab:

    col1, spacing, col2, spacing, col3 = st.columns([10,1,10,1,10])

    with col1:
        df_table = df_dict[4]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[4]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)

    with col2:
        df_table = df_dict[5]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[5]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)

    with col3:
        df_table = df_dict[6]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[6]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)





with summer_tab:

    col1, spacing, col2, spacing, col3 = st.columns([10,1,10,1,10])

    with col1:
        df_table = df_dict[7]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[7]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)

    with col2:
        df_table = df_dict[8]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[8]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)

    with col3:
        df_table = df_dict[9]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[9]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)





with autumn_tab:
    
    col1, spacing, col2, spacing, col3 = st.columns([10,1,10,1,10])

    with col1:
        df_table = df_dict[10]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[10]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)

    with col2:
        df_table = df_dict[11]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[11]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)

    with col3:
        df_table = df_dict[12]
        month_short = df_table.index[0].strftime("%b")

        df_plot = prepare__df_hourly_heatmap(df_table)
        fig_hourly_heatmap = create__fig_hourly_heatmap(df=df_plot, label_hrs=no_hrs)
        st.plotly_chart(fig_hourly_heatmap, use_container_width=True)

        df_table_typday = df_dict__typ_day[12]
        fig_hourly_typday = create__typ_day__line_chart(df=df_table_typday, month=month_short)
        st.plotly_chart(fig_hourly_typday, use_container_width=True)





with top_col2:

    # Example values for the color scale - adjust these according to your actual scale
    floor, ceiling, step = 0, 40, 5  
    gradient_values = list(range(floor, ceiling + 1, step))

    # These colors need to be chosen to approximate the 'hot_r' scale as closely as possible
    gradient_colors = ['#fee5d9', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603', '#7f2704']


    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown("###### Color Scale Legend (kWh)")


    # Start a container div for the horizontal layout of color containers
    legend_html = "<div style='display: flex; align-items: center; justify-content: start; flex-wrap: nowrap;'>"

    # Append each color box and label in a vertical container div to the horizontal container div
    for value in gradient_values:
        color_index = int((value - floor) / (ceiling - floor) * (len(gradient_colors) - 1))
        color = gradient_colors[color_index]
        legend_html += (
            "<div style='display: flex; flex-direction: column; align-items: center; margin-right: 5px;'>"
            f"<div style='width: 25px; height: 20px; background-color: {color};'>&nbsp;</div>"
            f"<span style='font-size: 12px;'>{value}</span>"
            "</div>"
        )


    # Close the container div
    legend_html += "</div>"

    # Display the horizontal legend
    st.markdown(legend_html, unsafe_allow_html=True)
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




# Variables to store the selections
data_sources = ["Local", "FTP", "GitHub"]
FTP_PATH    = r'https://absrd.xyz/streamlit_apps/SW__energy_use/data/'


datasource_col_1, datasource_col_2 = st.columns([1,1])

with datasource_col_1:

    source_choice = st.radio(
        label='Choose data source',
        options=['Upload a CSV file', 'Use sample data from FTP'],
        index=1, help=None, on_change=None,  horizontal=False,
        captions=None, label_visibility="visible",
        )

with datasource_col_2:
    # File uploader widget
    uploaded_file = st.file_uploader('Upload a CSV file', type='csv')



if source_choice == 'Upload a CSV file':

    if uploaded_file is not None:

        # Button to trigger data processing
        process_button = st.button('Process Data')
        if process_button:
            df = pd.read_csv(uploaded_file)

            # Process the data
            df_hourly, df_daily, df_monthly = process_data(df)
            st.success('Data has been processed from the uploaded CSV file')


            ##### ##### ##### ##### ##### ##### ##### #####
            st.session_state['df_hourly']   = df_hourly
            st.session_state['df_daily']    = df_daily
            st.session_state['df_monthly']  = df_monthly

            st.markdown('---')
            with st.expander('Data preview'):
                df_table = df.drop(['Account Number', 'MPAN', 'Meter Serial Number'], axis=1)
                st.dataframe(df_table)

        else:
            st.warning('Please upload data and click to process')


else:
    with datasource_col_1:
        st.markdown(f'###### FTP Path: {FTP_PATH}')

    csv_file_path = FTP_PATH + 'SWA_ConsumptionStatement_2023.01.01-2024.07.08.csv'
    df = pd.read_csv(
        csv_file_path,
        encoding='ISO-8859-1',
        keep_default_na=False, na_values=['NaN'],
        )

    # Process the data
    df_hourly, df_daily, df_monthly = process_data(df)
    st.success('Data has been processed from the uploaded CSV file')


    ##### ##### ##### ##### ##### ##### ##### #####
    st.session_state['df_hourly']   = df_hourly
    st.session_state['df_daily']    = df_daily
    st.session_state['df_monthly']  = df_monthly

    st.markdown('---')
    with st.expander('Data preview'):
        df_table = df.drop(['Account Number', 'MPAN', 'Meter Serial Number'], axis=1)
        st.dataframe(df_table)

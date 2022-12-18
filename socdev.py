import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Facebook Insight Summary',
                    page_icon=':bar_chart:',
                    layout='wide'
)
@st.cache
def get_data_from_excel(): # this fuction will prevent to call everytime our dataframe
    df = pd.read_excel(
        io='data/facebook.xlsx',
        engine='openpyxl',
        sheet_name='facebook',
        skiprows=2,
        usecols='A:I',
        nrows=274,
    )
    return df
df = get_data_from_excel() # this commond will will the data, without call fulldat


# ---- SIDEBAR -----
st.sidebar.header('Please Filter Here:')
Service = st.sidebar.multiselect(
    'Select the Service:',
    options=df['Service'].unique(),
    default=df['Service'].unique()
)

#st.sidebar.header('Please Filter Here:')
Location = st.sidebar.multiselect(
    'Select the Location:',
    options=df['Location'].unique(),
    default=df['Location'].unique()
)


# Make interactive by selection type
df_selection = df.query(
    'Service ==@Service & Location == @Location'
)

#st.dataframe(df_selection)

# ----- MAIN PAGE ---------
st.title(":bar_chart: Facebook Insight Summary 2022")
st.markdown('##')

# TOP KPIS
total_likes = int(df_selection['Likes'].sum())
average_likes = round(df_selection['Likes'].mean())
star_likes = ":star:" * int(round(average_likes, 0))
average_likes_by_service = round(df_selection['Likes'].mean(),2)

# Insert figure by selecting the position
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Total Likes:')
    st.subheader(f' {total_likes:,}')
with middle_column:
    st.subheader('Average Likes:')
    st.subheader(f' {average_likes:,}')
with right_column:
    st.subheader('Average likes by Service:')
    st.subheader(f' {average_likes_by_service:,}')

## Add some dividers
st.markdown('---')

## Services by Likes

service_by_like = (
    df_selection.groupby(by=['Service']).sum()[['Likes']].sort_values(by='Likes')
)


fig_service = px.bar(
    service_by_like,
    x="Likes",
    y=service_by_like.index,
    title='<b>Service by Likes</b>',
    color_discrete_sequence=["#0083B8"] * len(service_by_like),
    template="plotly_white",
)

st.plotly_chart(fig_service)


# --- HIDE STREAMLIT STYLES ----
hide_st_style = """
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            header {visibility:hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

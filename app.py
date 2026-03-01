from numpy import insert
import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff



df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df =preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('olympic_logo.png', width=120)


user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athelete wise Analysis')
)

if user_menu == 'Overall Analysis':
    st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
 
    selected_country = st.sidebar.selectbox('Select Country', country)
    

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally') 

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
   
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Overall Performance of ' + selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' performance in ' + str(selected_year) + ' Olympics') 
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]  
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]


    st.title('Top Statistics')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Host Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)

    with col3:
        st.header('Nations')
        st.title(nations)
    


    
if user_menu == 'Overall Analysis':
        events_over_time = helper.data_over_time(df, 'Event')       # Create dataframe that counts number of events per year | # Passing 'Event' tells helper function what to count
        fig = px.line(events_over_time, x='Edition', y= 'Event')
        st.title("Events over the years")                            # Title shown above second graph
        st.plotly_chart(fig)                                               # Display second interactive graph



        nations_over_time = helper.participating_nations_over_time(df)
        fig = px.line(nations_over_time, x='Edition', y= 'No of Countries')      # Create a line graph using Plotly | # X-axis = Edition (Year) | # Y-axis = Number of participating nations
        st.title("Participating Nations over the years")                # Title shown above first graph
        st.plotly_chart(fig)                                             # Display first interactive graph



        Atheletes_over_time = helper.data_over_time(df, 'Name')       # Create dataframe that counts number of athletes per year | # Passing 'Name' tells helper function what to count
        fig = px.line(Atheletes_over_time, x='Edition', y= 'Name')      # Create another line graph |  # X-axis = Edition (Year) | # Y-axis = Athlete count 
        st.title("Atheletes over the years ")                            # Title shown above third graph
        st.plotly_chart(fig)                                               # Display third interactive graph
    
        st.title("No of Events over time(Every Sport)")
        fig, ax = plt.subplots(figsize=(20, 20)) 
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax = sns.heatmap(x.pivot_table(index = 'Sport', columns = 'Year', values = 'Event', aggfunc='count').fillna(0).astype('int'),annot=True)
        st.pyplot(fig)

        
if user_menu == 'Country-wise Analysis':                 # Create a new section in the app for country-wise analysis
        st.sidebar.title('Country-wise Analysis')                 # Title for the country-wise analysis section
        country_list = df['region'].dropna().unique().tolist()     # Create a list of unique countries from the dataframe, dropping any NaN values | # This will be used to populate the dropdown menu for country selection
        country_list.sort()                              # Sort the list of countries alphabetically
        country_list.insert(0, 'Overall')                 # Insert 'Overall' at the beginning of the list to allow users to select it as an option
        selected_country = st.sidebar.selectbox('Select a Country', country_list)     # Create a dropdown menu in Streamlit for users to select a country | # The options in the dropdown are from the country_list we created
       
       

        country_df = helper.yearwise_medal_tally(df, selected_country)      
        fig = px.line(country_df, x='Year', y='Medal')                        # Create a line graph using Plotly to show the medal tally of the selected country over time | # x='Year' → years on X-axis | # y='Medal' → medal count on Y-axis 
        st.title(selected_country + ' Medal Tally over the years')              # Title for the graph, showing which country's medal tally is being displayed
        st.plotly_chart(fig)                                                    # Display the interactive graph in Streamlit

       
        st.title("Top 15 Atheletes of " + selected_country)     # Title for the table showing the top 15 athletes of the selected country
        top15_df = helper.most_successful_countrywise(df, selected_country)     # Call the helper function to get a dataframe with the top 15 athletes of the selected country based on their medal count | # This function takes the original dataframe and the selected country as input and returns a new dataframe with the top 15 athletes from that country
        st.table(top15_df)     # Display the dataframe as a table in Streamlit


if user_menu == 'Athelete wise Analysis':
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=650)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)  
    fig, ax = plt.subplots()
    
    ax: plt.Axes = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60)
    st.pyplot(fig)


    st.title('Men vs Women Participation Over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=650)
    st.plotly_chart(fig)
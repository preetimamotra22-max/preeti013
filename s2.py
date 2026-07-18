import streamlit as st
import plotly.express as px 
import pandas as pd
    
st.set_page_config(page_title="COVID-19 DATA ANALYSIS",page_icon=":heart:",layout="wide")
df=pd.read_csv("covid.csv")
df.info()

with st.sidebar:
    menu=st.sidebar("Menu",options=["Home","Dataset","Visualization","Dashboard"],icons=["house","file-text","activity","bare-chart"],default_index=0)

if menu=="Home":
    st.title("🦠COVID-19 DATA ANALYSIS")

    st.header("COVID-19")
    st.image("https://www.emeraldgrouppublishing.com/sites/default/files/image/covid-cells.jpg")
    st.write("""
    **COVID-19** stands for **Coronavirus Disease 2019**. 
    It is a contagious disease caused by the **SARS-CoV-2** virus.
    **How it spreads**: Through respiratory droplets from coughing, sneezing, or close contact.  
    **Common Symptoms**: Fever, cough, tiredness, loss of taste/smell, difficulty breathing.  
    """)
    # 3. OBJECTIVE
    st.header("🎯 Objective")
    st.image("https://media.istockphoto.com/id/1259038860/photo/coronavirus-2019-ncov-and-creative-chart.jpg")
    st.markdown("""
            The objective of this COVID-19 Dashboard is to:
    - **Collect & Clean Data**: Load covid dataset and handle missing values.
    - **Visualize Trends**: Show confirmed cases, deaths, and recoveries using interactive charts.
    - **Compare Regions**: Analyze impact across countries and over time.
    - **Derive Insights**: Calculate fatality rate, recovery rate, and active cases.
    """) 


if  menu=="Dataset":
   st. header("  Dataset")
   c1,c2,c3=st.tabs(["Data","Info","Description"])
   with c1:
        st.dataframe(df)
   with c2:
       st.write(df.columns)
   with c3:
       st.table(df.describe())
elif menu=="Visualization":
    st.title(" visualization")

# GRAPH 1: BUBBLE CHART - 4 dimensions
    st.header("1. Bubble: Death Rate vs Recovery Rate")
    fig1 = px.scatter(df, 
                      x="Deaths / 100 Cases", 
                      y="Recovered / 100 Cases",
                      size="Confirmed",
                      color="WHO Region",
                      hover_name="Country/Region",
                      size_max=60)
    st.plotly_chart(fig1, use_container_width=True)
    
    
    
    # GRAPH 2: TREEMAP - Hierarchy
    st.header("2. Treemap: Cases by WHO Region > Country")
    fig2 = px.treemap(df, 
                      path=['WHO Region', 'Country/Region'], 
                      values='Confirmed',
                      color='Confirmed',
                      color_continuous_scale='Reds')
    st.plotly_chart(fig2, use_container_width=True)
    
    # GRAPH 3: SUNBURST - 3 levels
    st.header("3. Sunburst: Region > Deaths Rate ")
    df['Death_Bucket'] = pd.cut(df['Deaths / 100 Cases'], bins=[0,2,5,10,30], labels=['Low','Medium','High','Very High'])
    fig3 = px.sunburst(df, path=['WHO Region', 'Deaths'], values='Deaths',
                       color='Deaths', color_continuous_scale='OrRd')
    st.plotly_chart(fig3, use_container_width=True)
    
    # GRAPH 4: HORIZONTAL BAR - Unique metric
    st.header("4. Top 10: Deaths per 100 Recovered")
    top10_deadly = df.sort_values("Deaths / 100 Recovered", ascending=False).head(10)
    fig4 = px.bar(top10_deadly, x="Deaths / 100 Recovered", y="Country/Region", 
                  orientation='h', color="Deaths / 100 Recovered", color_continuous_scale='Magma')
    st.plotly_chart(fig4, use_container_width=True)
    
    # GRAPH 5: AREA CHART - Momentum
    st.header("5. Area: Top 15 Countries by 1 Week % Increase")
    growth = df.sort_values("1 week % increase", ascending=False).head(15)
    fig5 = px.area(growth, x="Country/Region", y="1 week % increase",
                   color="WHO Region", line_group="WHO Region")
    fig5.update_xaxes(tickangle=-45)
    st.plotly_chart(fig5, use_container_width=True)
    
    # GRAPH 6: VIOLIN PLOT - Distribution by Region
    st.header("6. Violin: Distribution of Confirmed Cases by WHO Region")
    fig6 = px.violin(df, x="WHO Region", y="Confirmed", box=True, points="all",
                     color="WHO Region")
    st.plotly_chart(fig6, use_container_width=True)
    
    # GRAPH 7: FUNNEL CHART - Case Flow
    st.header("7. Funnel: Confirmed > Active > Recovered > Deaths")
    totals = {
        "Stage": ["Confirmed", "Active", "Recovered", "Deaths"],
        "Count": [df['Confirmed'].sum(), df['Active'].sum(), df['Recovered'].sum(), df['Deaths'].sum()]
    }
    funnel_df = pd.DataFrame(totals)
    fig7 = px.funnel(funnel_df, x="Count", y="Stage", title="Global Case Funnel")
    st.plotly_chart(fig7, use_container_width=True)
    
    
    # MAP 
    st.header("🌍 World Map: Confirmed Cases by Country")
    
    # Plotly needs country names. Your "Country/Region" works directly
    fig_map = px.choropleth(df,
                            locations="Country/Region",
                            locationmode="country names",  # tells plotly this column has country names
                            color="Confirmed",
                            hover_name="Country/Region",
                            hover_data=["Deaths", "Recovered", "Active", "Deaths / 100 Cases"],
                            color_continuous_scale="Reds",
                            title="Global Confirmed COVID-19 Cases")
    
    fig_map.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # 2 MORE MAP OPTIONS
    st.header("🗺️ More Map Views")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Deaths Map")
        fig_deaths = px.choropleth(df,
                                   locations="Country/Region",
                                   locationmode="country names",
                                   color="Deaths",
                                   hover_name="Country/Region",
                                   color_continuous_scale="OrRd")
        st.plotly_chart(fig_deaths, use_container_width=True)
    
    with col2:
        st.header("Active Cases by Country")
        fig_active = px.choropleth(df,
                                   locations="Country/Region",
                                   locationmode="country names",
                                   color="Active",
                                   hover_name="Country/Region",
                                   hover_data=["Confirmed", "Deaths", "Active"],
                                   color_continuous_scale="Blues",
                                   title="Global Active COVID-19 Cases")
        fig_active.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
        st.plotly_chart(fig_active, use_container_width=True)
        st.caption("Dark blue = More Active Cases. Shows where virus is currently spreading")
    
    with col2:
        st.header("Recovered Cases by Country") 
        fig_recovered = px.choropleth(df,
                                      locations="Country/Region",
                                      locationmode="country names",
                                      color="Recovered",
                                      hover_name="Country/Region",
                                      hover_data=["Confirmed", "Recovered", "Recovered / 100 Cases"],
                                      color_continuous_scale="Greens",
                                      title="Global Recovered COVID-19 Cases")
        fig_recovered.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
        st.plotly_chart(fig_recovered, use_container_width=True)
        st.caption("Dark green = More Recoveries. Shows healthcare success")
    
    # BONUS: SIDE BY SIDE COMPARISON
    st.markdown("---")
    st.header("📊 Active vs Recovered Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        top_active = df.sort_values("Active", ascending=False).head(10)
        fig_bar1 = px.bar(top_active, x="Country/Region", y="Active", 
                          color="Active", color_continuous_scale="Blues",
                          title="Top 10 Countries - Active Cases")
        fig_bar1.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_bar1, use_container_width=True)
    
    with col2:
        top_recovered = df.sort_values("Recovered", ascending=False).head(10)
        fig_bar2 = px.bar(top_recovered, x="Country/Region", y="Recovered", 
                          color="Recovered", color_continuous_scale="Greens",
                          title="Top 10 Countries - Recovered Cases")
        fig_bar2.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_bar2, use_container_width=True)
    
    
    st.title("Dashboard")
    
    st.title("❤️ COVID-19 DATA ANALYSIS")
    
    # ============ TOP SEARCH BAR ============
    search_col1, search_col2 = st.columns([3,1])
    with search_col1:
        country_search = st.text_input("🔍 Search Country Name", placeholder="Type: India, USA, Pakistan...")
    with search_col2:
        country_select = st.selectbox("Or Select", ["All"] + sorted(df['Country/Region'].unique()))

# FILTER DATA
    if country_search:
        df_view = df[df['Country/Region'].str.contains(country_search, case=False, na=False)]
    elif country_select!= "All":
        df_view = df[df['Country/Region'] == country_select]
    else:
        df_view = df
    
    # ============ KPI SECTION - UPDATES WITH SEARCH ============
    st.header("📊 Global Summary" if len(df_view) > 1 else f"📍 {df_view.iloc[0]['Country/Region']} Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Confirmed", f"{df_view['Confirmed'].sum():,}")
    col2.metric("Deaths", f"{df_view['Deaths'].sum():,}")
    col3.metric("Recovered", f"{df_view['Recovered'].sum():,}")
    col4.metric("Active", f"{df_view['Active'].sum():,}")
    
    st.markdown("---")
    
    # ============ MENU ============
    menu = st.sidebar.radio("Menu", ["Dataset", "Visualization", "Maps"])
    

if menu == "Dataset":
    st.header("Dataset")
tab1, tab2, tab3 = st.tabs(["Data", "Info", "Description"])

with tab1:
        st.write(f"Showing {len(df_view)} of {len(df)} countries")
        st.dataframe(df_view, use_container_width=True, height=500)

with tab2:
        st.write("**Shape:**", df_view.shape)
        st.write("**Columns:**", df_view.columns.tolist())
        st.write("**Missing:**")
        st.write(df_view.isnull().sum())
        with tab3:
            st.table(df_view.describe().T)


if menu == "Visualization":
     st.header("📈 Graphs for Selected Country/Countries")
    top = df_view.sort_values("Confirmed", ascending=False).head(10)
    fig1 = px.bar(top, x="Country/Region", y="Confirmed", color="Confirmed",
                          color_continuous_scale="Reds", title="Top Confirmed Cases")
    fig1.update_xaxes(tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)
        
            # Scatter
    fig2 = px.scatter(df_view, x="Deaths / 100 Cases", y="Recovered / 100 Cases",
                              size="Confirmed", color="WHO Region", hover_name="Country/Region")
    st.plotly_chart(fig2, use_container_width=True)
        
    menu == "Maps"
    st.header("🌍  Map")
    fig_map = px.choropleth(df_view, locations="Country/Region", locationmode="country names",
                                    color="Confirmed", hover_name="Country/Region",
                                    color_continuous_scale="Reds")
    st.plotly_chart(fig_map, use_container_width=True)
        
        
        
    st.header("📈 Pie Chart Visualizations")
            
        col1, col2 = st.columns(2)
            
            # 1.  covid 19  PIE - Confirmed vs Deaths vs Recovered vs Active
        with col1:
                st.subheader("Covid-19 cases")
                total_data = {
                    'Status': ['Confirmed', 'Deaths', 'Recovered', 'Active'],
                    'Count': [
                        df_view['Confirmed'].sum(),
                        df_view['Deaths'].sum(),
                        df_view['Recovered'].sum(), 
                        df_view['Active'].sum()
                    ]
                }
                total_df = pd.DataFrame(total_data)
                
                fig1 = px.pie(total_df, values='Count', names='Status', 
                              hole=0.4, color_discrete_sequence=['#FF4B4B','#8B0000','#00CC96','#636EFA'])
                fig1.update_traces(textinfo='percent+label')
                fig1.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white")
                st.plotly_chart(fig1, use_container_width=True)
            
            # 2. TOP 10 COUNTRIES PIE
        with col2:
                st.subheader("Top 10 Countries by Confirmed")
                top10 = df_view.sort_values("Confirmed", ascending=False).head(10)
                
                fig2 = px.pie(top10, values='Confirmed', names='Country/Region',
                              color_discrete_sequence=px.colors.sequential.Reds)
                fig2.update_traces(textinfo='percent+label', textposition='inside')
                fig2.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white")
                st.plotly_chart(fig2, use_container_width=True)
            
            # 3. WHO REGION PIE
                st.subheader("Cases by WHO Region")
                region_df = df_view.groupby('WHO Region')['Confirmed'].sum().reset_index()
                fig3 = px.pie(region_df, values='Confirmed', names='WHO Region',
                                  color_discrete_sequence=px.colors.qualitative.Set3)
                fig3.update_traces(textinfo='percent+label')
                fig3.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white")
                st.plotly_chart(fig3, use_container_width=True)
                
        

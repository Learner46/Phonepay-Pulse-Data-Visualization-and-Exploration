

import os
import json 
import pandas as pd
import mysql.connector
import streamlit as st
import  plotly.express as px 
import  plotly.graph_objects as go
from streamlit_option_menu import option_menu
import requests



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""

 

)

print(mydb)
mycursor = mydb.cursor(buffered=True)



#mycursor.execute("create database phonepay_data ")

mycursor.execute("use phonepay_data")


#1. Aggregated_transsaction

mycursor.execute(" select * from aggregated_transaction")
mydb.commit()
table1= mycursor.fetchall()

Aggre_transaction = pd.DataFrame(table1,columns = ("States","Years","Quarter","Transaction_type","Transaction_count",
                                                    "Transaction_amount"))


#2. Aggregated_user

mycursor.execute("select * from aggregated_user ")
mydb.commit()
table2= mycursor.fetchall()

Aggre_user = pd.DataFrame(table2, columns = ("States", "Years","Quarter","Brands","Transaction_count", "Percentage"))


#3. Map Transaction

mycursor.execute("select * from map_transaction")
mydb.commit()
table3 = mycursor.fetchall()

Map_transaction = pd.DataFrame(table3, columns = ("States", "Years","Quarter", "Districts","Transaction_count",
                                                   "Transaction_amount" ))

#4. Map user 

mycursor.execute("select * from map_user ")
mydb.commit()
table4= mycursor.fetchall()

map_user = pd.DataFrame(table4 , columns = ( "States", "Years","Quarter","Districts", "RegisteredUser", "AppOpens" ))


# 5. Top Trancsaction

mycursor.execute("select * from top_transaction")
mydb.commit()
table5 = mycursor.fetchall()

top_transaction = pd.DataFrame( table5, columns = ("States", "Years","Quarter","Entity_Name","Transaction_count","Transaction_amount"))

# 6. Top User

mycursor.execute("select * from top_user ")
mydb.commit()
table6 = mycursor.fetchall()

Top_user = pd.DataFrame(table6, columns = ("States", "Years","Quarter","Districts", "RegisteredUser"))


#Streamlit portion 

st.title ("📱 PhonePay Data Visualization And Exploration 📈!")
st.divider()



def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    ag_trans = df_state.groupby("Transaction_type",)[["Transaction_count","Transaction_amount"]].sum()
    ag_trans.reset_index(inplace= True)

    st.subheader(f"Selected State: {state}", divider= "rainbow")
    st.write("DataFrame for the selected state:")
    st.write(df_state)
    

    col1,col2= st.columns(2)

    with col1:
        
         fig_hbar_1= px.bar(ag_trans, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
         st.plotly_chart(fig_hbar_1)

    with col2:

         fig_hbar_2= px.bar(ag_trans, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
         
         st.plotly_chart(fig_hbar_2)  


st.subheader("Aggregated_transaction_Analysis_for States",divider= "rainbow")


# to Get unique states from the DataFrame
unique_states = Aggre_transaction["States"].unique()

# Get user input for state using a dropdown box
selected_state = st.selectbox("Select a state:", unique_states)

# Call the function with the selected state
Aggre_Transaction_type(Aggre_transaction, selected_state)

def aggre_transaction_y(df,year):
    ag_trans_y = df[df["Years"] == year]
    ag_trans_y.reset_index(drop= True, inplace =  True)

    ag_trans_yg = ag_trans_y.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    ag_trans_yg.reset_index(inplace = True)

    st.subheader(f"Selected year: {year}", divider= "rainbow")
    
    fig = px.choropleth(ag_trans_yg,
                         geojson= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                         featureidkey='properties.ST_NM',# Key to match states in GeoJSON with state names in DataFrame
                         locations='States',  # Column in DataFrame containing state names)
                         color='Transaction_count',
                         color_continuous_scale='Reds')
    
    fig.update_geos( fitbounds="locations",visible=False)
    st.plotly_chart(fig)
    
    fig1 = px.choropleth(ag_trans_yg,
                         geojson= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                         featureidkey='properties.ST_NM',# Key to match states in GeoJSON with state names in DataFrame
                         locations='States',  # Column in DataFrame containing state names)
                         color='Transaction_amount',
                         color_continuous_scale='Reds')
    
    fig1.update_geos( fitbounds="locations",visible=False)
    st.plotly_chart(fig1)
        

st.subheader("Aggregated_transaction_Analysis_for_year",divider= "rainbow")



# to Get unique Years from the DataFrame
unique_year = Aggre_transaction["Years"].unique()

# Get user input for year using a dropdown box
selected_Year = st.selectbox("Select a year:", unique_year)

# Call the function with the selected year
aggre_transaction_y(Aggre_transaction, selected_Year)        



def aggre_user_plot_1(df,year):
    ag_user_yr=df[df["Years"] == year]
    ag_user_yr.reset_index(drop = True, inplace= True)

    ag_user_g= pd.DataFrame(ag_user_yr.groupby("Brands")["Transaction_count"].sum()).reset_index()

    st.subheader(f"Selected year: {year}", divider= "rainbow")
     

    fig_line_1= px.bar(ag_user_g, x = "Brands", y = "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                 width = 1000, color_discrete_sequence=px.colors.sequential.haline_r)
    
    st.plotly_chart(fig_line_1)

st.subheader("Aggregated_user_Analysis_for_year",divider= "rainbow")


# to Get unique Years from the DataFrame
unique_year = Aggre_user["Years"].unique()

# Get user input for year using a dropdown box
selected_Year = st.selectbox("Select a year:", unique_year)

# Call the function with the selected year
aggre_user_plot_1(Aggre_user, selected_Year)  


    

def aggre_user_plot_2(df,quarter):
    ag_user_q = df[df["Quarter"] == quarter]
    ag_user_q.reset_index(drop= True, inplace = True)

    fig_pie_1 = px.pie(data_frame= ag_user_q , names = "Brands", values= "Transaction_count", hover_data= "Percentage",
                       width=1000, title= " TRANSACTION COUNT PERCENTAGE", hole= 0.5,
                        color_discrete_sequence = px.colors.sequential.Magenta_r)
    
    st.plotly_chart(fig_pie_1)
    
#to Get unique Quarter from the DataFrame
unique_quarters = Aggre_user["Quarter"].unique()

# Get user input for quarter using a dropdown box
quarters = st.selectbox("quarter:", unique_quarters) 

st.subheader("Percentage_of_Aggregated_user_Analysis_of_the brands",divider= "rainbow")


aggre_user_plot_2(Aggre_user,quarters)   



def aggre_user_plot_3(df,state):
    ag_user_s = df[df["States"] == state]
    ag_user_s.reset_index(drop = True, inplace = True)

    ag_user_sg = pd.DataFrame(ag_user_s.groupby("Brands")["Transaction_count"].sum())
    ag_user_sg.reset_index(inplace= True)
    st.subheader(f"Selected State: {state}", divider= "rainbow")

    fig_scatter_1 = px.line(ag_user_sg, x = "Brands", y = "Transaction_count", markers= True, width=1000)
    st.plotly_chart(fig_scatter_1)


st.subheader("Aggregated_user_analysis_for_state",divider= "rainbow")


# to Get unique states from the DataFrame
unique_states = Aggre_user["States"].unique()

# Get user input for state using a dropdown box
selected_state = st.selectbox("Select a state:", unique_states,  key="state_selector")

# Call the function with the selected state
aggre_user_plot_3(Aggre_user, selected_state)


def Map_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    map_trans = df_state.groupby("Districts",)[["Transaction_count","Transaction_amount"]].sum()
    map_trans.reset_index(inplace= True)
    

    st.subheader(f"Selected State: {state}", divider= "rainbow")
    
    
    

    col1,col2= st.columns(2)

    with col1:
        
         fig_hbar_1= px.bar(map_trans, x= "Transaction_count", y= "Districts", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} District - TRANSACTION COUNT",height= 500)
         st.plotly_chart(fig_hbar_1)

    with col2:

         fig_hbar_2= px.bar(map_trans, x= "Transaction_amount", y= "Districts", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} District -  TRANSACTION AMOUNT", height= 500)
         
         st.plotly_chart(fig_hbar_2)  


st.subheader("Map_transaction_Analysis_for States",divider= "rainbow")


# to Get unique states from the DataFrame
unique_states = Map_transaction["States"].unique()

# Get user input for state using a dropdown box
selected_state = st.selectbox("Select a state:", unique_states, key="state_selector1")

# Call the function with the selected state
Map_Transaction_type(Map_transaction, selected_state)

def Map_user_plot_1(df,year):
    map_user_y=df[df["Years"] == year]
    map_user_y.reset_index(drop= True, inplace= True)

    map_user_yg = map_user_y.groupby("States")[["RegisteredUser", "AppOpens"]].sum().reset_index()

    st.subheader(f"Selected year: {year}", divider= "rainbow") 


    fig_map_user_plot_1 = px.line(map_user_yg, x = "States", y = ["RegisteredUser","AppOpens"], markers = True,
                                  width= 1000, height=800, title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    
    st.plotly_chart(fig_map_user_plot_1)

st.subheader("Map_user_Analysis_for_year",divider= "rainbow")


# to Get unique Years from the DataFrame
unique_year = map_user["Years"].unique()

# Get user input for year using a dropdown box
selected_Year = st.selectbox("Select a year:", unique_year, key="Year_selector1" )

# Call the function with the selected year
Map_user_plot_1(map_user, selected_Year)  


def map_user_plot_3(df,state):
    map_user_s = df[df["States"] == state]
    map_user_s.reset_index(drop= True, inplace = True)
    
    map_user_sg = map_user_s.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum().reset_index()
    st.subheader(f"Selected State: {state}", divider= "rainbow") 
    

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(map_user_sg, x ="RegisteredUser", y = "Districts", orientation="h",
                                    title = f"{state.upper()} REGISTERED USER", height= 800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)  
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(map_user_sg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2) 

st.subheader("Map_User_Analysis_for States",divider= "rainbow")


# to Get unique states from the DataFrame
unique_states = map_user["States"].unique()

# Get user input for state using a dropdown box
selected_state = st.selectbox("Select a state:", unique_states, key="state_selector2")

# Call the function with the selected state
map_user_plot_3(map_user, selected_state)   


def Top_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    Top_trans = df_state.groupby("Entity_Name",)[["Transaction_count","Transaction_amount"]].sum()
    Top_trans.reset_index(inplace= True)

    st.subheader(f"Selected State: {state}", divider= "rainbow")
    
    
    

    col1,col2= st.columns(2)

    with col1:
        
         fig_hbar_1= px.bar(Top_trans, x= "Transaction_count", y= "Entity_Name", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} Entities - TOP TRANSACTION COUNT",height= 500)
         st.plotly_chart(fig_hbar_1)

    with col2:

         fig_hbar_2= px.bar(Top_trans, x= "Transaction_amount", y= "Entity_Name", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} Entities - TOP TRANSACTION AMOUNT", height= 500)
         
         st.plotly_chart(fig_hbar_2)  


st.subheader("Top_transaction_Analysis_for States",divider= "rainbow")


# to Get unique states from the DataFrame
unique_states = top_transaction["States"].unique()

# Get user input for state using a dropdown box
selected_state = st.selectbox("Select a state:", unique_states, key="state_selector3")

# Call the function with the selected state
Top_Transaction_type(top_transaction, selected_state)


def top_user_plot_1(df,year):
    top_user_y= df[df["Years"] == year]
    top_user_y.reset_index(drop = True, inplace=True)

    top_user_yg=pd.DataFrame(top_user_y.groupby(["States","Quarter"])["RegisteredUser"].sum()).reset_index()
    st.subheader(f"Selected year: {year}", divider= "rainbow")

    fig_top_plot_1 = px.bar(top_user_yg ,x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    
    st.plotly_chart(fig_top_plot_1)

st.subheader("Top_user_Analysis_for_year",divider= "rainbow")


# to Get unique Years from the DataFrame
unique_year = Top_user["Years"].unique()

# Get user input for year using a dropdown box
selected_Year = st.selectbox("Select a year:", unique_year, key="Year_selector2" )

# Call the function with the selected year
top_user_plot_1(Top_user, selected_Year)  

def top_user_plot_2(df,state):
    top_user_state = df[df["States"] == state]
    top_user_state.reset_index(drop = True, inplace= True)

    top_user_sg = pd.DataFrame(top_user_state.groupby("Districts")["RegisteredUser"].sum()).reset_index()
    st.subheader(f"Selected State: {state}", divider= "rainbow")
    

    fig_top_plot_1= px.bar(top_user_sg, x= "Districts", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "Districts",hover_data="RegisteredUser",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

st.subheader("Top_User_Analysis_for States",divider= "rainbow")


# to Get unique states from the DataFrame
unique_states = Top_user["States"].unique()

# Get user input for state using a dropdown box
selected_state = st.selectbox("Select a state:", unique_states, key="state_selector4")

# Call the function with the selected state
top_user_plot_2(Top_user, selected_state)

#question part

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1=brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names = "Brands", 
                        color_discrete_sequence= px.colors.sequential.dense_r, title="Top Mobile Brands of Transaction_count")
    
    return st.plotly_chart(fig_brands)

def ques2():
    ltm = Aggre_transaction[["States","Transaction_amount"]]
    lt1= ltm.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts = px.bar(lt2, x = "States", y = "Transaction_amount", title = " STATES WITH LOWEST TRANSACTION AMOUNT",
                      color_discrete_sequence= px.colors.sequential.Oranges_r)
    
    return st.plotly_chart(fig_lts)

def ques3():
    
    dhtm= Map_transaction[["Districts", "Transaction_amount"]]
    htm1= dhtm.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending= False)
    htm2= pd.DataFrame(htm1).head(10).reset_index()

    fig_htm= px.pie(htm2, values="Transaction_amount", names = "Districts", title= "TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                     color_discrete_sequence=px.colors.sequential.Emrld_r)
    
    return st.plotly_chart(fig_htm)


def ques4():
     
    dltm =Map_transaction[["Districts", "Transaction_amount"]]
    dlm1= dltm.groupby("Districts") ["Transaction_amount"].sum().sort_values(ascending= False)
    dlm2= pd.DataFrame(dlm1).head(10).reset_index()

    fig_dlm= px.pie(dlm2, values= "Transaction_amount" , names = "Districts", title = "Top 10 Districts With Lowest Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    
    return st.plotly_chart(fig_dlm)
    
def ques5():
    
    st_appopens= map_user[["States", "AppOpens"]]
    sa1=st_appopens.groupby("States") ["AppOpens"].sum().sort_values(ascending= False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x ="States", y = "AppOpens", title = "Top 10 States With AppOpens",
                    color_discrete_sequence= px.colors.sequential.deep_r)
    
    return st.plotly_chart(fig_sa)

def ques6():
     
    lo_appopens= map_user[["States", "AppOpens"]]
    lap1= lo_appopens.groupby("States") ["AppOpens"].sum().sort_values(ascending=True)
    lap2= pd.DataFrame(lap1).reset_index().head(10)
    
    fig_lap= px.bar(lap2, x="States" , y ="AppOpens", title = "Lowest 10 States With AppOpens",
                     color_discrete_sequence=px.colors.sequential.dense_r)
    
    return st.plotly_chart(fig_lap)

def ques7():
    
    sltc=Aggre_transaction[["States", "Transaction_count"]]
    ltc1= sltc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    ltc2= pd .DataFrame(ltc1).reset_index()

    fig_ltc= px.bar(ltc2, x = "States", y = "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                     color_discrete_sequence=px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_ltc) 

def ques8():
    
    shtc=Aggre_transaction[["States", "Transaction_count"]]
    htc1= shtc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    htc2= pd.DataFrame(htc1).reset_index()

    fig_htc= px.bar(htc2, x = "States", y = "Transaction_count", title= "STATES WITH  HIGHEST  TRANSACTION COUNT",
                     color_discrete_sequence=px.colors.sequential.Magenta_r)
    
    return st.plotly_chart(fig_htc) 

def ques9():
     
     shta=Aggre_transaction[["States", "Transaction_amount"]]
     shta1=shta.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
     shta2=pd.DataFrame(shta1).reset_index()

     fig_ta=px.bar(shta2, x = "States", y = "Transaction_amount", title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
     
     return st.plotly_chart(fig_ta)
    
def ques10():

     dlta= Map_transaction[["Districts", "Transaction_amount"]]    
     dlt1=dlta.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
     dlt2= pd.DataFrame(dlt1).reset_index().head(50)


     fig_lta=px.bar(dlt2, x = "Districts", y = "Transaction_amount", title ="DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                     color_discrete_sequence= px.colors.sequential.Mint_r)
     
     return st.plotly_chart(fig_lta)
     


select= option_menu("Main Menu",["Please select the question below"]) 


if select == "Please select the question below":

    ques= st.selectbox("**Select the Question**",('Click Here','Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    

if ques=="Top Brands Of Mobiles Used":
        ques1()

elif ques=="States With Lowest Trasaction Amount":
           ques2()

elif ques=='Districts With Highest Transaction Amount':
            ques3()
     
elif ques=='Top 10 Districts With Lowest Transaction Amount':
            ques4()

elif ques=='Top 10 States With AppOpens':
            ques5()

elif ques=='Least 10 States With AppOpens':
            ques6()

elif ques=='States With Lowest Trasaction Count':
            ques7()

elif ques=='States With Highest Trasaction Count':
            ques8()

elif ques=='States With Highest Trasaction Amount':
            ques9()   

elif ques=='Top 50 Districts With Lowest Transaction Amount':
            ques10() 


#done 








    



















        
         














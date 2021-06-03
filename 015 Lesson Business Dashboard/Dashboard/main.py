import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="expanded", )
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


import streamlit.components.v1 as components



# Load the available data and overview

url="data/dataonline.csv"




st.sidebar.header("Amazure Online Shop")

data = st.sidebar.file_uploader("Upload Dataset", type=['csv', 'txt', 'xlsx'])
if data is not None:
        df = pd.read_csv(data)
        df = pd.read_csv(url, encoding="ISO-8859-1", low_memory=False)
        df["Revenue"] = df["UnitPrice"] * df["Quantity"]
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        df["InvoiceMonth"] = pd.DatetimeIndex(df["InvoiceDate"]).month
        df["InvoiceYear"] = pd.DatetimeIndex(df["InvoiceDate"]).year

else:

    df = pd.read_csv(url, encoding="ISO-8859-1", low_memory=False)
    df["Revenue"] = df["UnitPrice"] * df["Quantity"]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["InvoiceMonth"] = pd.DatetimeIndex(df["InvoiceDate"]).month
    df["InvoiceYear"] = pd.DatetimeIndex(df["InvoiceDate"]).year


# Use the full page instead of a narrow central column


menu = ['Business Snapshot','Analysis','About']
selection = st.sidebar.selectbox("Key Performance Indicator (KPI) ", menu)

st.sidebar.write('Retail analytics is the process of providing analytical data on inventory levels, supply chain movement, consumer demand, sales, etc. ... The analytics on demand and supply data can be used for maintaining procurement level and also for taking marketing decisions.')

if selection== 'Business Snapshot':
    # Use the full page instead of a narrow central column
    #st.beta_set_page_config(layout="wide")
    st.markdown('Display data')
    st.table(df.head())

    col1, col2 = st.beta_columns(2)


    with col1:
        st.header("Monthly Revenue Overview Bar ")
        df_revenue = df.groupby(["InvoiceMonth", "InvoiceYear"])["Revenue"].sum().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="Revenue", hue="InvoiceYear", data=df_revenue)
        plt.title("Monthly Revenue")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        st.pyplot(plt)

    with col2:
        # Monthly Items Sold Overview
        st.header("Monthly Items Sold Overview")
        df_quantity = df.groupby(["InvoiceMonth", "InvoiceYear"])["Quantity"].sum().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="Quantity", data=df_quantity)
        plt.title("Monthly Items Sold")
        plt.xlabel("Month")
        plt.ylabel("Items Sold")
        st.pyplot(plt)



    col3, col4 = st.beta_columns(2)


    with col3:
        st.header("Monthly Active Customers")
        # Monthly Active Customers
        df_active = df.groupby(["InvoiceMonth", "InvoiceYear"])["CustomerID"].nunique().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="CustomerID", hue="InvoiceYear", data=df_active)
        plt.title("Monthly Active Users")
        plt.xlabel("Month")
        plt.ylabel("Active Users")
        st.pyplot(plt)

    with col4:
        # Monthly Items Sold Overview
        st.header("Average Revenue per Month")
        df_revenue_avg = df.groupby(["InvoiceMonth", "InvoiceYear"])["Revenue"].mean().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="Revenue", data=df_revenue)
        plt.title("Monthly Average Revenue ")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        st.pyplot(plt)

    # New vs Existing Users
    st.header("New vs Existing Users")
    df_first_purchase = df.groupby(["CustomerID"])["InvoiceDate"].min().reset_index()
    df_first_purchase.columns = ["CustomerID", "FirstPurchaseDate"]
    df = pd.merge(df, df_first_purchase, on="CustomerID")
    df["UserType"] = "New"
    df.loc[df["InvoiceDate"] > df["FirstPurchaseDate"], "UserType"] = "Existing"

    df.head()
    # New vs Existing User Revenue Analysis
    df_new_revenue = df.groupby(["InvoiceMonth", "InvoiceYear", "UserType"])["Revenue"].sum().reset_index()
    plt.figure()
    sns.relplot(x="InvoiceMonth", y="Revenue", hue="UserType", data=df_new_revenue, kind="line", height=12,
                aspect=18 / 10)
    plt.title("New vs Existing Customer Revenue Overview")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    st.pyplot(plt)



if selection== 'Analysis':

    st.markdown('Display data')
    st.write(df.head())

    # shape of data
    if st.checkbox("show shape "):
        # number =st.number_input("number of rows to view ")
        st.write('Data Shape')
        st.write('{:,} rows; {:,} columns'.format(df.shape[0], df.shape[1]))

        # data description
        st.markdown("Descriptive statistics ")
        st.write(df.describe())












# adding html  Template

footer_temp = """
	 <!-- CSS  -->
	  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	  <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" type="text/css" rel="stylesheet" media="screen,projection"/>
	  <link href="static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
	   <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
	 <footer class="page-footer grey darken-4">
	    <div class="container" id="aboutapp">
	      <div class="row">
	        <div class="col l6 s12">
	          <h5 class="white-text">About Streamlit Africa Data School</h5>
	          <p class="grey-text text-lighten-4">Streamlit Practical.</p>
	        </div>

	   <div class="col l3 s12">
	          <h5 class="white-text">Connect With Me</h5>
	          <ul>
	            <a href="https://www.facebook.com/AfricaDataSchool/" target="_blank" class="white-text">
	            <i class="fab fa-facebook fa-4x"></i>
	          </a>
	          <a href="https://www.linkedin.com/company/africa-data-school" target="_blank" class="white-text">
	            <i class="fab fa-linkedin fa-4x"></i>
	          </a>
	          <a href="https://www.youtube.com/watch?v=ZRdlQwNTJ7o" target="_blank" class="white-text">
	            <i class="fab fa-youtube-square fa-4x"></i>
	          </a>
	           <a href="https://github.com/Africa-Data-School" target="_blank" class="white-text">
	            <i class="fab fa-github-square fa-4x"></i>
	          </a>
	          </ul>
	        </div>
	      </div>
	    </div>
	    <div class="footer-copyright">
	      <div class="container">
	      Made by <a class="white-text text-lighten-3" href="https://africadataschool.com/">John </a><br/>
	      <a class="white-text text-lighten-3" href="https://africadataschool.com/"></a>
	      </div>
	    </div>
	  </footer>

	"""

if selection== 'About':
    st.subheader("About App")
    components.html(footer_temp, height=500)
# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(" :cup_with_straw: Customize Your Smoothie!  :cup_with_straw:")
st.write(
    """Choose the firsts you want in your custom Smoothie!
    """)

name_on_order =st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be: ",name_on_order)



#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#    index=None,
#    placeholder="Select fruit ",
#)

#st.write("Your favorite fruit is:", option)


#session = get_active_session()
cnx = st.connection("snowflake")
session =cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list =st.multiselect('Choose upto 5 ingredients:'
                                 , my_dataframe
                                 ,max_selections=5
                                )
    
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        
    st.write(ingredients_string)  


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+ name_on_order  +"""')"""

    time_to_insert = st.button('Submit Order')
    #st.write(my_insert_stmt)

    if ingredients_string and time_to_insert:
     session.sql(my_insert_stmt).collect()
    
    st.success('Your Smoothie is ordered '+ name_on_order, icon="✅")

import streamlit as st
from agent import agent_executor

# Streamlit app title and description
st.title("👕 Weather-Based Clothing Recommendation")
st.markdown("What should I wear today based on the weather? Enter your city, and we'll recommend!")

# Input box for the user to type the city name
city = st.text_input("Enter city name", placeholder="Istanbul, Ankara, Izmir...")

# Button to trigger the recommendation
if st.button("Get Recommendation"):
    if not city:
        # Warning if no city is provided
        st.warning("Please enter a city name.")
    else:
        try:
            # Call the agent to get weather and clothing recommendation
            result = agent_executor.invoke(
                {"input": f"Get the weather for {city} and recommend appropriate clothing."}
            )
            st.success("Here are your personalized recommendations 👇")
            st.markdown(result["output"])
        except Exception as e:
            # Display error if something goes wrong
            st.error("An error occurred.")
            st.code(str(e), language="bash")


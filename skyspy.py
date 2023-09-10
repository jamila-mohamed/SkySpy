
import streamlit as st
import joblib
import pandas as pd
import time as t
import datetime
from datetime import datetime, time
import os
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

# Load the trained GBR model and inputs
Model = joblib.load('Model.pkl')
Inputs = joblib.load('Inputs.pkl')

def prediction(airline, source, destination, duration, total_stops, additional_info, day_of_journey_num, month_of_journey_num, day_of_arrival_num, month_of_arrival_num, departure, arrival, duration_categorized, departure_period, arrival_period, holiday, trip_distance):
    
    # Create a DataFrame with the same columns as the training data
    test_df = pd.DataFrame(columns = Inputs)
    
    # Set the values for each column based on the function arguments
    test_df.at[0, 'Airline'] = airline
    test_df.at[0, 'Source'] = source
    test_df.at[0, 'Destination'] = destination
    test_df.at[0, 'Duration'] = duration
    test_df.at[0, 'Total_Stops'] = total_stops
    test_df.at[0, 'Additional_Info'] = additional_info
    test_df.at[0, 'Day_of_Journey_Num'] = day_of_journey_num
    test_df.at[0, 'Month_of_Journey_Num'] = month_of_journey_num
    test_df.at[0, 'Day_of_Arrival_Num'] = day_of_arrival_num
    test_df.at[0, 'Month_of_Arrival_Num'] = month_of_arrival_num
    test_df.at[0, 'Departure'] = departure
    test_df.at[0, 'Arrival'] = arrival
    test_df.at[0, 'Duration_Categorized'] = duration_categorized
    test_df.at[0, 'Departure_Period'] = departure_period
    test_df.at[0, 'Arrival_Period'] = arrival_period
    test_df.at[0, 'Holiday'] = holiday
    test_df.at[0, 'Trip_distance'] = trip_distance
    
    # Predict the price using the model
    price = Model.predict(test_df)[0]
    return price

def get_distance(source, destination):
    # Create a geolocator object
    geolocator = Nominatim(user_agent="skyspy")
    
    # Get the location data for the source and destination cities
    source_location = geolocator.geocode(source)
    destination_location = geolocator.geocode(destination)
    
    # Get the latitude and longitude coordinates for the source and destination cities
    source_coords = (source_location.latitude, source_location.longitude)
    destination_coords = (destination_location.latitude, destination_location.longitude)
    
    # Calculate the distance between the cities using the great_circle function
    distance = great_circle(source_coords, destination_coords).kilometers
    
    return round(distance, 2)

def get_trip_distance_category(distance):
    if distance <= 622.83:
        return 'Short_Dist'
    elif distance <= 1358.31:
        return 'Medium_Dist'
    else:
        return 'Long_Dist'

def get_period(hour):
    
    if hour in range(6, 12):
        return 'Morning'
    elif hour in range(12, 18):
        return 'Afternoon'
    elif hour in range(18, 21):
        return 'Evening'
    else:
        return 'Night'

def get_duration_category(duration):
    
    if duration <= 750:
        return 'Short_duration'
    elif duration <= 1500:
        return 'Medium_duration'
    else:
        return 'Long_duration'    

def main():
    
    # Define the input categories
    airlines = ['Air India', 'Jet Airways', 'IndiGo', 'SpiceJet', 'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia']
    sources = ['Kolkata', 'Delhi', 'Banglore', 'Chennai', 'Mumbai']
    destinations = ['Banglore', 'Cochin', 'New Delhi', 'Kolkata', 'Delhi', 'Hyderabad']
    additional_info = ['No info', 'In-flight meal not included', 'No check-in baggage included']
    
    # Define the list of holiday dates
    holidays = ['06-18', '06-20', '06-21', '06-29', '07-03', '07-29', '08-06', '08-15', '08-16', '08-20', '08-29', '08-30',
                '09-06', '09-07', '09-19', '09-23', '09-28', '10-02', '10-15', '10-20', '10-21', '10-22', '10-23', '10-24',
                '10-28', '10-31']
    
    # Create the Streamlit app
    st.set_page_config(page_title = "SkySpy")
    
    st.sidebar.image("static/skyspy-logo.png")
    
    st.sidebar.markdown("<h4 style='text-align: center;'>Your Ultimate Guide to Smarter Airfares</h4>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;'>Experience a stress-free journey with our app - no hidden costs!</p>", unsafe_allow_html=True)

    if 'first_run' not in st.session_state:
        st.session_state['first_run'] = True
        
    if st.session_state['first_run']:
        text = st.empty()
        text.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 80vh;'><h1 style='text-align: center; font-size: 100px; color: #EC3928;'>SkySpy</h1></div>", unsafe_allow_html=True)
        t.sleep(2)
        text.empty()
        st.session_state['first_run'] = False
        
    st.markdown("<h4 style='text-align: center;'>Simply fill in a few details to easily compare airfares from different airlines and find yourself the best deal.</h4>", unsafe_allow_html=True)
    st.markdown("---")
    st.write()
    
    # Create input fields for the user
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>Which airline would you like to fly with?</span></div>", unsafe_allow_html=True)
    airline = st.selectbox('Airline:', airlines, label_visibility= 'collapsed')
    
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>From which city would you like to depart?</span></div>", unsafe_allow_html=True)
    source = st.selectbox('Source:', sources, label_visibility= 'collapsed')
    
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>To which city would you like to travel?</span></div>", unsafe_allow_html=True)
    destination = st.selectbox('Destination:', destinations, label_visibility= 'collapsed')
    
    # Calculate the distance between the source and destination cities
    distance = get_distance(source, destination)
     
    # Calculate the trip distance category from the distance using get_trip_distance_category function.
    trip_distance = get_trip_distance_category(distance)
    
    # Create a dropdown menu for selecting the number of stops
    total_stops_options = ['non-stop', '1 stop', '2 stops', '3 stops']
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>How many stops do you prefer for your flight?</span></div>", unsafe_allow_html=True)
    total_stops_index = st.selectbox('Total Stops:', total_stops_options, label_visibility= 'collapsed')
    total_stops = total_stops_options.index(total_stops_index)
    
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>Do you have any additional information or preferences regarding your flight?</span></div>", unsafe_allow_html=True)
    additional_info = st.selectbox('Additional Info:', additional_info, label_visibility= 'collapsed')
    
    # Create a calendar widget for selecting the journey date
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>What is your expected departure date?</span></div>", unsafe_allow_html=True)
    journey_date = st.date_input('Journey Date:', label_visibility= 'collapsed')
    day_of_journey_num = journey_date.day
    month_of_journey_num = journey_date.month
    
    # Check if the journey date is a holiday
    if journey_date.strftime('%m-%d') in holidays:
        holiday = 'Yes'
    else:
        holiday = 'No'
    
    # Create a calendar widget for selecting the arrival date
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>What is your expected arrival date?</span></div>", unsafe_allow_html=True)
    arrival_date = st.date_input('Arrival Date:', label_visibility= 'collapsed')
    day_of_arrival_num = arrival_date.day
    month_of_arrival_num = arrival_date.month
    
    # Create a time input widget for selecting the departure time
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>What is your preferred departure time?</span></div>", unsafe_allow_html=True)
    departure_time = st.time_input('Departure Time:', value=time(12, 0), label_visibility= 'collapsed')
    departure_seconds = departure_time.hour * 3600 + departure_time.minute * 60 + departure_time.second
    
    # Calculate the departure period from the departure time hour using get_period function.
    departure_period = get_period(departure_time.hour)
    
    # Create a time input widget for selecting the arrival time
    st.markdown("<div style='text-align: center;'><span style='font-size: 19px;'>What is your preferred arrival time?</span></div>", unsafe_allow_html=True)
    arrival_time = st.time_input('Arrival Time:', value=time(12, 0), label_visibility= 'collapsed')
    arrival_seconds = arrival_time.hour * 3600 + arrival_time.minute * 60 + arrival_time.second
    
    # Calculate the arrival period from the arrival time hour using get_period function
    arrival_period = get_period(arrival_time.hour)
    
    # Calculate the duration from the departure and arrival times
    duration_seconds = (arrival_time.hour * 3600 + arrival_time.minute * 60 + arrival_time.second) - (departure_time.hour * 3600 + departure_time.minute * 60 + departure_time.second)
    duration = duration_seconds / 60
    
    # Calculate the duration category from the duration minutes using get_duration_category function.
    duration_categorized = get_duration_category(duration)

    style = "<style>.row-widget.stButton {text-align: center; color: #EC3928}</style>"
    st.markdown(style, unsafe_allow_html=True)
    
    # Predict the price when the Predict button is clicked
    if st.button('Price me up!💲'):
        
        # Call the prediction function with the values from the input fields
        price = prediction(airline, source, destination, duration, total_stops, additional_info, day_of_journey_num, month_of_journey_num, day_of_arrival_num, month_of_arrival_num, departure_seconds, arrival_seconds, duration_categorized, departure_period, arrival_period, holiday, trip_distance)
        
        # Display the predicted price
        st.write("<div style='text-align: center;'><h5 style='color: #EC3928;'>Based on our analysis, this ticket should cost around ₹{}.</h5></div>".format(round(price)), unsafe_allow_html=True)

if __name__ == '__main__':
    main()

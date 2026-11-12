
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Weather Forecast | Krishi Saarthi",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Live Weather Forecast")
st.caption("Weather information to support smarter farming decisions.")

st.divider()


# Find location coordinates
def get_coordinates(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    place = data["results"][0]

    return {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "name": place["name"],
        "country": place.get("country", "")
    }


# Get weather information
def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,precipitation,"
            "weather_code,wind_speed_10m"
        ),
        "daily": (
            "weather_code,temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "precipitation_sum"
        ),
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json()


# Weather code descriptions
def weather_description(code):

    descriptions = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Overcast ☁️",
        45: "Fog 🌫️",
        48: "Depositing Rime Fog 🌫️",
        51: "Light Drizzle 🌦️",
        53: "Moderate Drizzle 🌦️",
        55: "Dense Drizzle 🌧️",
        61: "Slight Rain 🌧️",
        63: "Moderate Rain 🌧️",
        65: "Heavy Rain 🌧️",
        71: "Slight Snow ❄️",
        73: "Moderate Snow ❄️",
        75: "Heavy Snow ❄️",
        80: "Rain Showers 🌦️",
        81: "Moderate Rain Showers 🌧️",
        82: "Heavy Rain Showers ⛈️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with Hail ⛈️",
        99: "Severe Thunderstorm ⛈️"
    }

    return descriptions.get(code, "Weather information unavailable")


# Location input
st.subheader("📍 Select Your Location")

city = st.text_input(
    "Enter Village / City / District",
    value="Phagwara"
)

if st.button("🔍 Get Weather Forecast", use_container_width=True):

    if not city.strip():
        st.warning("Please enter a location.")

    else:

        try:
            with st.spinner("Finding location..."):
                location = get_coordinates(city.strip())

            if location is None:
                st.error("Location not found. Try another city or district.")

            else:
                with st.spinner("Fetching latest weather data..."):
                    weather = get_weather(
                        location["latitude"],
                        location["longitude"]
                    )

                st.session_state.weather_data = weather
                st.session_state.weather_location = location

        except requests.RequestException as e:
            st.error(f"Weather service error: {e}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")


# Display weather
if "weather_data" in st.session_state:

    weather = st.session_state.weather_data
    location = st.session_state.weather_location

    current = weather["current"]
    daily = weather["daily"]

    st.divider()

    st.subheader(
        f"📍 {location['name']}, {location['country']}"
    )

    st.caption(
        f"Weather time: {current['time']} "
        f"| Timezone: {weather.get('timezone', 'Local')}"
    )

    st.subheader("🌤️ Current Weather")

    st.markdown(
        f"### {weather_description(current['weather_code'])}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Temperature",
        f"{current['temperature_2m']} °C",
        help="Current air temperature"
    )

    col2.metric(
        "Feels Like",
        f"{current['apparent_temperature']} °C"
    )

    col3.metric(
        "Humidity",
        f"{current['relative_humidity_2m']} %"
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "Wind Speed",
        f"{current['wind_speed_10m']} km/h"
    )

    col5.metric(
        "Current Precipitation",
        f"{current['precipitation']} mm"
    )

    st.divider()

    st.subheader("📅 7-Day Weather Forecast")

    forecast_df = pd.DataFrame({
        "Date": daily["time"],
        "Condition": [
            weather_description(code)
            for code in daily["weather_code"]
        ],
        "Max Temperature (°C)": daily["temperature_2m_max"],
        "Min Temperature (°C)": daily["temperature_2m_min"],
        "Rain Probability (%)": daily["precipitation_probability_max"],
        "Rainfall (mm)": daily["precipitation_sum"]
    })

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🌡️ Temperature Forecast")

    chart_df = pd.DataFrame({
        "Date": daily["time"],
        "Maximum": daily["temperature_2m_max"],
        "Minimum": daily["temperature_2m_min"]
    })

    st.line_chart(
        chart_df.set_index("Date")
    )

    st.subheader("🌱 Farming Advisory")

    st.info(
        "Use the rainfall forecast to plan irrigation. "
        "Check local field conditions before watering or applying "
        "fertilizers. Forecasts are estimates, not guarantees."
    )

    st.caption(
        "Weather data provided by Open-Meteo. "
        "Data licensed under CC BY 4.0."
    )

st.divider()
st.caption("KRISHI SAARTHI | Weather Intelligence")

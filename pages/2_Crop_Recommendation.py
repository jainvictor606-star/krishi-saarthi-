
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Crop Recommendation | Krishi Saarthi",
    page_icon="🌾",
    layout="wide"
)

MODEL_NAME = "gemini-3.5-flash"


def recommend_crops(details, language):
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(timeout=30000)
    )

    prompt = f"""
    You are KRISHI SAARTHI, an agricultural assistant.

    Recommend suitable crops using these farmer details:
    {details}

    Reply in {language}.

    Structure your answer as:
    1. Top 3 suitable crop options.
    2. Why each crop may suit these conditions.
    3. Approximate growing duration.
    4. Water and irrigation needs.
    5. Basic cultivation precautions.
    6. Information the farmer should verify locally.

    Important:
    - Do not guarantee yield, profit or success.
    - Do not invent local soil or weather data.
    - Clearly state assumptions and uncertainties.
    - Consider season, soil, water and budget together.
    - Recommend checking local agricultural university
      or KVK advice before final crop selection.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1500,
            temperature=0.4
        )
    )

    return response.text


st.title("🌾 Smart Crop Recommendation")
st.caption("Find suitable crops for your farming conditions.")

language = st.selectbox(
    "Select Response Language",
    ["English", "Hindi", "Punjabi"]
)

st.divider()

st.subheader("🚜 Enter Your Farm Details")

with st.form("crop_form"):

    location = st.text_input(
        "Village / City / District",
        placeholder="Example: Phagwara, Punjab"
    )

    col1, col2 = st.columns(2)

    with col1:
        land_area = st.number_input(
            "Land Area (Acres)",
            min_value=0.1,
            max_value=10000.0,
            value=2.0,
            step=0.1
        )

        soil_type = st.selectbox(
            "Soil Type",
            [
                "Alluvial Soil",
                "Sandy Soil",
                "Clay Soil",
                "Loamy Soil",
                "Black Soil",
                "Red Soil",
                "Unknown"
            ]
        )

        season = st.selectbox(
            "Current / Upcoming Season",
            [
                "Kharif",
                "Rabi",
                "Zaid",
                "Not Sure"
            ]
        )

    with col2:
        water = st.selectbox(
            "Water Availability",
            [
                "High",
                "Moderate",
                "Limited",
                "Rainfed Only"
            ]
        )

        budget = st.selectbox(
            "Approximate Farming Budget",
            [
                "Below ₹10,000",
                "₹10,000 - ₹25,000",
                "₹25,000 - ₹50,000",
                "₹50,000 - ₹1,00,000",
                "Above ₹1,00,000"
            ]
        )

        previous_crop = st.text_input(
            "Previous Crop (Optional)",
            placeholder="Example: Wheat"
        )

    soil_health = st.selectbox(
        "Soil Fertility (If Known)",
        [
            "Good",
            "Average",
            "Poor",
            "Not Tested"
        ]
    )

    submitted = st.form_submit_button(
        "🌱 Recommend Suitable Crops",
        use_container_width=True
    )


if submitted:

    if not location.strip():
        st.warning("Please enter your location.")

    else:
        details = {
            "Location": location,
            "Land Area": f"{land_area} acres",
            "Soil Type": soil_type,
            "Season": season,
            "Water Availability": water,
            "Budget": budget,
            "Previous Crop": previous_crop or "Not provided",
            "Soil Fertility": soil_health
        }

        with st.spinner("Analyzing your farming conditions..."):

            try:
                result = recommend_crops(
                    details,
                    language
                )

                st.success("Crop recommendations generated!")

                st.subheader("🌾 Your Personalized Crop Report")
                st.markdown(result)

            except Exception as e:
                st.error(
                    "Unable to generate recommendations. "
                    "Please try again."
                )
                st.caption(f"Error: {e}")


st.divider()
st.caption("KRISHI SAARTHI | Powered by Gemini AI")

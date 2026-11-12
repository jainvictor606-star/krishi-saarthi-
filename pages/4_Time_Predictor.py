
import streamlit as st
from google import genai
from google.genai import types
from datetime import date

st.set_page_config(
    page_title="Time Predictor | Krishi Saarthi",
    page_icon="⏳",
    layout="wide"
)

MODEL_NAME = "gemini-3.5-flash"


def predict_harvest(details, language):

    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(timeout=30000)
    )

    prompt = f"""
    You are KRISHI SAARTHI, an agricultural crop growth assistant.

    Analyze these farming details:
    {details}

    Reply in {language}.

    Prepare a crop harvesting estimation report containing:

    1. Expected crop growth duration in days.
    2. Estimated earliest harvesting date.
    3. Estimated most likely harvesting window.
    4. Estimated latest harvesting date.
    5. Important growth stages.
    6. Irrigation and crop-care suggestions.
    7. Weather conditions that may affect harvesting.
    8. Signs that indicate crop maturity.
    9. Factors that can delay or advance harvesting.

    Rules:
    - Calculate dates using the supplied sowing date.
    - Use realistic crop-duration ranges for the specified variety.
    - If the variety is unknown, state your assumption.
    - Never guarantee a harvesting date or yield.
    - Do not invent actual local weather information.
    - Clearly mention uncertainty.
    - Recommend verifying estimates with local agricultural experts.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1500,
            temperature=0.3
        )
    )

    return response.text


st.title("⏳ Smart Time Predictor")
st.caption("Estimate your crop's harvesting timeline with AI.")

st.divider()

st.subheader("🌾 Enter Crop Information")

language = st.selectbox(
    "Select Report Language",
    ["English", "Hindi", "Punjabi"]
)

with st.form("harvest_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        crop = st.selectbox(
            "Select Crop",
            [
                "Wheat",
                "Rice",
                "Maize",
                "Mustard",
                "Potato",
                "Tomato",
                "Cotton",
                "Sugarcane",
                "Pulses",
                "Other"
            ]
        )

        variety = st.text_input(
            "Crop Variety",
            placeholder="Example: HD 3086"
        )

        sowing_date = st.date_input(
            "Sowing Date",
            value=date.today()
        )

        location = st.text_input(
            "Village / District / State",
            placeholder="Example: Phagwara, Punjab"
        )

    with col2:

        soil = st.selectbox(
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

        irrigation = st.selectbox(
            "Irrigation Method",
            [
                "Drip Irrigation",
                "Sprinkler Irrigation",
                "Flood Irrigation",
                "Rainfed",
                "Other / Unknown"
            ]
        )

        water = st.selectbox(
            "Water Availability",
            [
                "High",
                "Moderate",
                "Limited"
            ]
        )

        crop_condition = st.selectbox(
            "Current Crop Condition",
            [
                "Recently Sown",
                "Seedling Stage",
                "Vegetative Stage",
                "Flowering Stage",
                "Fruiting / Grain Filling",
                "Near Maturity",
                "Not Sure"
            ]
        )

    extra_details = st.text_area(
        "Additional Information (Optional)",
        placeholder="Enter any crop growth observations..."
    )

    submitted = st.form_submit_button(
        "🔮 Predict Harvesting Time",
        use_container_width=True
    )


if submitted:

    if not location.strip():
        st.warning("Please enter your farming location.")

    elif sowing_date > date.today():
        st.warning("Please enter a sowing date that is not in the future.")

    else:

        details = {
            "Crop": crop,
            "Variety": variety or "Not specified",
            "Sowing Date": str(sowing_date),
            "Location": location,
            "Soil Type": soil,
            "Irrigation Method": irrigation,
            "Water Availability": water,
            "Current Crop Stage": crop_condition,
            "Additional Information": extra_details or "None"
        }

        with st.spinner(
            "AI is calculating your estimated harvesting timeline..."
        ):

            try:

                result = predict_harvest(
                    details,
                    language
                )

                st.success("Harvest prediction report generated!")

                st.divider()

                st.subheader("🌱 Your Harvest Prediction Report")

                st.markdown(result)

                st.info(
                    "This is an AI-generated estimate. "
                    "Actual harvesting depends on crop maturity, "
                    "weather, variety and field conditions."
                )

            except Exception as e:

                st.error(
                    "Unable to generate prediction. Please try again."
                )

                st.caption(f"Error: {e}")


st.divider()
st.caption("KRISHI SAARTHI | Powered by Gemini AI")

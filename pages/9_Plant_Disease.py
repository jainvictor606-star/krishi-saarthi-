
import streamlit as st
import io
import time
from PIL import Image
from google import genai

st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

MODEL_NAME = "gemini-3.5-flash"

# ---------------- PAGE DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: #F4F6EF;
}

h1, h2, h3 {
    color: #17452E;
}

.main-header {
    background: linear-gradient(120deg, #123B29, #39734B);
    padding: 25px;
    border-radius: 16px;
    color: white;
    margin-bottom: 20px;
}

.main-header h1 {
    color: white !important;
}

.tip-box {
    background: #E7F0E5;
    padding: 15px;
    border-radius: 12px;
    color: #17452E;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="main-header">
    <h1>🌿 Plant Disease Detection</h1>
    <p>AI-powered preliminary plant health analysis</p>
    <p>Your Trusted Partner in Smart Farming</p>
</div>
""", unsafe_allow_html=True)


# ---------------- LANGUAGE ----------------

language = st.selectbox(
    "Select Report Language",
    ["English", "Hindi", "Punjabi"]
)

language_instruction = {
    "English": "Respond in simple English.",
    "Hindi": "Respond in simple Hindi.",
    "Punjabi": "Respond in simple Punjabi."
}


# ---------------- IMAGE INPUT ----------------

st.subheader("📸 Upload Plant Image")

st.markdown("""
<div class="tip-box">
    Upload a clear photograph of the affected plant leaf.
    Good lighting and a focused image can improve the analysis.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a plant image",
    type=["jpg", "jpeg", "png", "webp"]
)

camera_image = st.camera_input("Or take a photo")

image_file = uploaded_file if uploaded_file else camera_image


# ---------------- ANALYSIS FUNCTION ----------------

def analyse_plant(image, language):

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an agricultural plant-health assistant.

    Analyse the uploaded plant image.

    {language_instruction[language]}

    Prepare a report with these sections:

    1. Plant Identification (if possible)
    2. Possible Disease or Condition
    3. Visible Symptoms
    4. Possible Causes
    5. General Treatment and Care Suggestions
    6. Prevention Tips
    7. When to Contact an Agricultural Expert

    Important instructions:

    - Do not claim a confirmed diagnosis from an image alone.
    - Explain uncertainty if the image is unclear.
    - Do not invent a disease if none is visible.
    - Avoid unsafe chemical mixing instructions.
    - Do not suggest unverified pesticide doses.
    - Prefer general plant-care and integrated pest-management advice.
    - Recommend expert confirmation for serious cases.
    """

    # Limited retries for temporary server errors
    max_attempts = 3

    for attempt in range(max_attempts):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt, image]
            )

            if not response.text:
                raise ValueError("The AI returned an empty response.")

            return response.text

        except Exception as error:

            error_message = str(error).upper()

            temporary_error = any(
                code in error_message
                for code in [
                    "503",
                    "UNAVAILABLE",
                    "500",
                    "502",
                    "504",
                    "429",
                    "RESOURCE_EXHAUSTED"
                ]
            )

            if temporary_error and attempt < max_attempts - 1:
                wait_time = 2 ** (attempt + 1)

                time.sleep(wait_time)
                continue

            raise error


# ---------------- DISPLAY IMAGE ----------------

if image_file:

    try:
        image = Image.open(
            io.BytesIO(image_file.getvalue())
        ).convert("RGB")

        st.image(
            image,
            caption="Selected Plant Image",
            use_container_width=True
        )

        st.write("")

        if st.button(
            "🔍 Analyse Plant",
            type="primary",
            use_container_width=True
        ):

            try:
                with st.spinner(
                    "🌱 AI is examining your plant image..."
                ):

                    result = analyse_plant(
                        image,
                        language
                    )

                st.success("Plant analysis completed!")

                st.subheader("📋 Plant Health Report")

                st.markdown(result)

                st.warning(
                    "This is a preliminary AI assessment, not a "
                    "confirmed diagnosis. Consult an agricultural "
                    "expert before making important treatment decisions."
                )

            except ValueError as error:
                st.error(str(error))

            except Exception as error:

                error_text = str(error).upper()

                if "503" in error_text or "UNAVAILABLE" in error_text:
                    st.error(
                        "Gemini AI service is temporarily busy. "
                        "Please try again after a few minutes."
                    )

                elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    st.error(
                        "AI request limit reached. Please wait before "
                        "trying again."
                    )

                elif "404" in error_text or "NOT_FOUND" in error_text:
                    st.error(
                        "The selected Gemini model may not be available. "
                        "Check the model name used in your working Kisan AI page."
                    )

                else:
                    st.error(
                        "Plant analysis could not be completed. "
                        "Please try again later."
                    )

    except Exception:
        st.error(
            "Unable to read this image. Please upload a valid JPG, "
            "PNG or WEBP photograph."
        )

else:
    st.info("Please upload a plant image or take a photo to begin.")

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "🌱 KRISHI SAARTHI | Your Trusted Partner in Smart Farming"
)

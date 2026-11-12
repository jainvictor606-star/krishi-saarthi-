
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import time

st.set_page_config(
    page_title="Kisan AI | Krishi Saarthi",
    page_icon="🌱",
    layout="wide"
)

MODEL_NAME = "gemini-3.5-flash"

# Gemini connection
def get_client():
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(timeout=30000)
    )


# Chatbot response
def get_gemini_response(question, language):
    client = get_client()

    prompt = f"""
    You are Kisan AI, a helpful agricultural assistant.
    Help farmers with crops, irrigation, soil, fertilizers,
    farming techniques and government agriculture schemes.

    Reply in {language}.
    Give practical, easy-to-understand and safe advice.
    Do not invent facts. Mention uncertainty when necessary.

    Farmer's question: {question}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1000,
            temperature=0.5
        )
    )
    return response.text


# Plant image analysis
def analyze_plant_image(image, language):
    client = get_client()

    prompt = f"""
    You are Kisan Saarthi Plant Health Assistant.

    Analyze the uploaded plant or leaf photograph.
    Reply in {language}.

    Provide:
    1. Plant identification, if possible.
    2. Visible symptoms.
    3. Possible disease or pest, if identifiable.
    4. Possible causes.
    5. Prevention methods.
    6. Suggested next steps for the farmer.

    Important:
    - Do not claim certainty from an unclear image.
    - If the image is insufficient, request clearer photos.
    - Do not recommend unsafe chemical use.
    - Recommend consulting a local agriculture expert
      before applying pesticides or other treatments.
    - Clearly distinguish visual observations from possibilities.
    """

    image_part = types.Part.from_bytes(
        data=image.getvalue(),
        mime_type=image.type
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt, image_part],
        config=types.GenerateContentConfig(
            max_output_tokens=1200,
            temperature=0.3
        )
    )

    return response.text


# Header
st.title("🌱 Kisan AI")
st.caption("Your Smart Agricultural Assistant")

language = st.selectbox(
    "Choose your language",
    ["English", "Hindi", "Punjabi"]
)

st.divider()

# Two sections
chat_tab, image_tab = st.tabs(
    ["💬 Ask Kisan AI", "📸 Plant Disease Detection"]
)

# CHAT SECTION
with chat_tab:
    st.subheader("Ask your farming question")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask anything about farming...")

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Kisan AI is thinking..."):
                try:
                    answer = get_gemini_response(
                        question, language
                    )
                    st.markdown(answer)

                except Exception as e:
                    answer = (
                        "Sorry, Kisan AI is temporarily unavailable. "
                        "Please try again."
                    )
                    st.error(f"Gemini error: {e}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# IMAGE ANALYSIS SECTION
with image_tab:
    st.subheader("🌿 Check Your Plant Health")

    st.write(
        "Upload a clear photograph of a plant or leaf "
        "to check its visible health symptoms."
    )

    uploaded_image = st.file_uploader(
        "Upload plant image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_image:
        try:
            image = Image.open(uploaded_image)
            st.image(
                image,
                caption="Uploaded Plant Image",
                width=350
            )

            if st.button("🔍 Analyze Plant"):
                with st.spinner(
                    "Gemini AI is analyzing your plant..."
                ):
                    try:
                        result = analyze_plant_image(
                            uploaded_image,
                            language
                        )

                        st.success("Analysis completed!")
                        st.markdown("### 🌱 Plant Health Report")
                        st.markdown(result)

                    except Exception as e:
                        st.error(
                            f"Image analysis failed: {e}"
                        )

        except Exception:
            st.error("Please upload a valid image.")

    else:
        st.info(
            "Upload a JPG, JPEG, PNG or WEBP plant photograph."
        )

st.divider()
st.caption("KRISHI SAARTHI | Powered by Gemini AI")

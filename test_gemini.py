
import streamlit as st
import time
from google import genai
from google.genai import types

st.title("🌱 Krishi Saarthi - Gemini Auto Test")

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite"
]

def test_model(client, model):

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=model,
                contents="Reply only: Krishi Saarthi AI is working!",
                config=types.GenerateContentConfig(
                    max_output_tokens=100
                )
            )

            if response.text:
                return response.text

        except Exception as e:
            error = str(e)

            if "503" in error or "UNAVAILABLE" in error:
                if attempt == 0:
                    time.sleep(3)
                    continue

            raise e

    return None


if st.button("Test Gemini AI"):

    try:
        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"],
            http_options=types.HttpOptions(timeout=20000)
        )

        for model in MODELS:

            st.write(f"Testing: {model}")

            try:
                answer = test_model(client, model)

                if answer:
                    st.success(f"Connected: {model}")
                    st.write(answer)
                    break

            except Exception as e:
                st.warning(f"{model} failed: {e}")

        else:
            st.error("All tested models are temporarily unavailable.")

    except Exception as e:
        st.error(f"Setup Error: {e}")

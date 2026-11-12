
import streamlit as st
import pandas as pd
import requests
import time

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Live Mandi Rates | Krishi Saarthi",
    page_icon="🌾",
    layout="wide"
)

API_URL = (
    "https://api.data.gov.in/resource/"
    "9ef84268-d588-465a-a308-a864a43d0070"
)

PAGE_SIZE = 100
MAX_RECORDS = 2000


# =====================================================
# API KEY
# =====================================================

try:
    API_KEY = st.secrets["DATA_GOV_API_KEY"]
except Exception:
    API_KEY = None


# =====================================================
# API REQUEST
# =====================================================

def make_api_request(params):

    for attempt in range(2):

        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=(15, 45),
                headers={
                    "User-Agent": "KrishiSaarthi/1.0"
                }
            )

            response.raise_for_status()
            data = response.json()

            if not isinstance(data, dict):
                return None, "Invalid API response."

            if "records" not in data:
                return None, "Records field not found."

            return data, None

        except requests.exceptions.Timeout:

            if attempt == 0:
                time.sleep(2)
                continue

            return None, "Government API timeout. Please retry."

        except requests.exceptions.HTTPError as e:

            status = (
                e.response.status_code
                if e.response is not None
                else "Unknown"
            )

            return None, f"API HTTP Error: {status}"

        except requests.exceptions.RequestException as e:
            return None, f"Connection error: {e}"

        except ValueError:
            return None, "Invalid JSON response."

    return None, "API request failed."


# =====================================================
# FETCH ALL AVAILABLE PAGES
# =====================================================

@st.cache_data(ttl=300, show_spinner=False)
def fetch_mandi_data(state):

    all_records = []
    offset = 0
    total_records = None

    while offset < MAX_RECORDS:

        params = {
            "api-key": API_KEY,
            "format": "json",
            "limit": PAGE_SIZE,
            "offset": offset,
            "filters[state]": state
        }

        data, error = make_api_request(params)

        if error:
            return None, error, len(all_records), total_records

        records = data.get("records", [])

        if total_records is None:
            try:
                total_records = int(data.get("total", 0))
            except (ValueError, TypeError):
                total_records = 0

        if not records:
            break

        all_records.extend(records)

        offset += len(records)

        if len(records) < PAGE_SIZE:
            break

        if total_records and offset >= total_records:
            break

    if not all_records:
        return pd.DataFrame(), None, 0, total_records or 0

    df = pd.DataFrame(all_records)

    df.columns = [
        str(col).strip().lower()
        for col in df.columns
    ]

    # Clean text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Convert prices
    for col in ["min_price", "max_price", "modal_price"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df, None, len(df), total_records


# =====================================================
# FILTER HELPERS
# =====================================================

def get_options(df, column):

    if column not in df.columns:
        return []

    values = (
        df[column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    values = values[
        (values != "")
        & (values.str.lower() != "nan")
    ]

    # Preserve original display values
    return sorted(
        values.unique().tolist(),
        key=lambda x: x.casefold()
    )


def apply_filter(df, column, selected_value):

    if selected_value == "All" or column not in df.columns:
        return df.copy()

    selected_normalized = selected_value.strip().casefold()

    return df[
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        == selected_normalized
    ].copy()


def format_price(value):

    if pd.isna(value):
        return "N/A"

    return f"₹{value:,.0f}"


# =====================================================
# HEADER
# =====================================================

st.title("🌾 Live Mandi Rates")

st.markdown(
    "### Agricultural Market Price Information"
)

st.write(
    "Find available crop prices, districts and agricultural markets."
)

st.caption(
    "Data Source: Government of India – AGMARKNET / data.gov.in"
)

st.divider()


# =====================================================
# API KEY CHECK
# =====================================================

if not API_KEY:

    st.error(
        "DATA_GOV_API_KEY not found in secrets.toml."
    )

    st.stop()


# =====================================================
# STATE SELECTION
# =====================================================

states = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Delhi",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
]

st.subheader("📍 Select Location")

selected_state = st.selectbox(
    "State",
    states,
    index=states.index("Punjab"),
    key="mandi_state"
)


# =====================================================
# REFRESH DATA
# =====================================================

if st.button("🔄 Refresh Mandi Data"):

    fetch_mandi_data.clear()
    st.rerun()


# =====================================================
# FETCH DATA
# =====================================================

with st.spinner(
    f"Loading mandi records for {selected_state}..."
):

    df, error, loaded_count, total_records = fetch_mandi_data(
        selected_state
    )

if error:

    st.error(error)
    st.stop()

if df is None or df.empty:

    st.warning(
        f"No mandi records found for {selected_state}."
    )

    st.stop()


# =====================================================
# DATA STATUS
# =====================================================

st.success(
    f"Successfully loaded {loaded_count} records!"
)

st.caption(
    f"Total records reported by API: {total_records} | "
    f"Records loaded: {loaded_count}"
)

if total_records and loaded_count < total_records:

    st.info(
        "Some records may remain unavailable because of the "
        "configured maximum fetch limit."
    )


# =====================================================
# DYNAMIC DISTRICT FILTER
# =====================================================

st.divider()

st.subheader("🔎 Filter Mandi Records")

district_options = get_options(df, "district")

selected_district = st.selectbox(
    "Select District",
    ["All"] + district_options,
    key="mandi_district"
)

district_df = apply_filter(
    df,
    "district",
    selected_district
)


# =====================================================
# DYNAMIC COMMODITY FILTER
# =====================================================

commodity_options = get_options(
    district_df,
    "commodity"
)

selected_commodity = st.selectbox(
    "Select Crop / Commodity",
    ["All"] + commodity_options,
    key="mandi_commodity"
)

commodity_df = apply_filter(
    district_df,
    "commodity",
    selected_commodity
)


# =====================================================
# DYNAMIC MARKET FILTER
# =====================================================

market_options = get_options(
    commodity_df,
    "market"
)

selected_market = st.selectbox(
    "Select Market",
    ["All"] + market_options,
    key="mandi_market"
)

filtered_df = apply_filter(
    commodity_df,
    "market",
    selected_market
)


# =====================================================
# FINAL FILTERED RESULTS
# =====================================================

st.divider()

st.subheader("📊 Mandi Price Overview")

st.caption(
    f"Showing {len(filtered_df)} matching records."
)

if filtered_df.empty:

    st.warning(
        "No matching records found. Please select different filters."
    )

else:

    # -------------------------------------------------
    # PRICE METRICS
    # -------------------------------------------------

    c1, c2, c3 = st.columns(3)

    if "min_price" in filtered_df.columns:

        c1.metric(
            "Average Minimum Price",
            format_price(filtered_df["min_price"].mean())
        )

    if "max_price" in filtered_df.columns:

        c2.metric(
            "Average Maximum Price",
            format_price(filtered_df["max_price"].mean())
        )

    if "modal_price" in filtered_df.columns:

        c3.metric(
            "Average Modal Price",
            format_price(filtered_df["modal_price"].mean())
        )

    # -------------------------------------------------
    # DATA TABLE
    # -------------------------------------------------

    st.divider()

    st.subheader("📋 Mandi Records")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------------------------------
    # PRICE CHART
    # -------------------------------------------------

    if (
        "market" in filtered_df.columns
        and "modal_price" in filtered_df.columns
    ):

        chart_df = filtered_df[
            ["market", "modal_price"]
        ].dropna()

        if not chart_df.empty:

            chart_df = (
                chart_df
                .groupby("market")["modal_price"]
                .mean()
                .sort_values(ascending=False)
            )

            st.subheader("📈 Market-wise Modal Price")

            st.bar_chart(chart_df)

    # -------------------------------------------------
    # CSV DOWNLOAD
    # -------------------------------------------------

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download Mandi Records",
        data=csv_data,
        file_name="krishi_saarthi_mandi_rates.csv",
        mime="text/csv",
        use_container_width=True
    )


# =====================================================
# DATA INFORMATION
# =====================================================

st.divider()

with st.expander("ℹ️ Data Information"):

    st.write("Selected State:", selected_state)
    st.write("Selected District:", selected_district)
    st.write("Selected Commodity:", selected_commodity)
    st.write("Selected Market:", selected_market)

    st.write("Records loaded:", loaded_count)
    st.write("Matching records:", len(filtered_df))
    st.write("Total records reported by API:", total_records)

    st.caption(
        "The displayed prices and arrival dates are taken from "
        "the records returned by the Government API."
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        <h3>🌱 KRISHI SAARTHI</h3>
        <p>Your Trusted Partner in Smart Farming</p>
        <small>Empowering Farmers Through Technology</small>
    </div>
    """,
    unsafe_allow_html=True
)

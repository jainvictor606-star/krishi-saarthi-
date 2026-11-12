
import streamlit as st

st.set_page_config(
    page_title="Government Schemes",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Government Schemes & Updates")
st.caption("Discover government support programmes for Indian farmers")

st.info(
    "Explore agricultural schemes, their objectives and official "
    "government portals. Always verify current eligibility and application "
    "dates on the official website."
)

schemes = [
    {
        "name": "PM-KISAN",
        "category": "Financial Support",
        "description": "Provides eligible landholding farmer families with "
                       "₹6,000 per year through Direct Benefit Transfer, "
                       "subject to scheme rules and exclusions.",
        "benefits": "Income support in three instalments.",
        "eligibility": "Eligible landholding farmer families; exclusions apply.",
        "link": "https://pmkisan.gov.in/",
        "icon": "💰"
    },
    {
        "name": "Pradhan Mantri Fasal Bima Yojana",
        "category": "Crop Insurance",
        "description": "Provides crop insurance protection against specified "
                       "natural risks and crop losses under notified conditions.",
        "benefits": "Financial protection against covered crop losses.",
        "eligibility": "Farmers growing notified crops in notified areas.",
        "link": "https://pmfby.gov.in/",
        "icon": "🌾"
    },
    {
        "name": "Pradhan Mantri Krishi Sinchayee Yojana",
        "category": "Irrigation",
        "description": "Promotes improved irrigation and water-use efficiency, "
                       "including micro-irrigation.",
        "benefits": "Supports efficient use of water in agriculture.",
        "eligibility": "Depends on the component and state implementation.",
        "link": "https://pmksy.gov.in/",
        "icon": "💧"
    },
    {
        "name": "Soil Health Card Scheme",
        "category": "Soil Health",
        "description": "Provides information about soil nutrients and "
                       "recommendations for balanced fertiliser use.",
        "benefits": "Helps farmers understand soil condition and nutrient needs.",
        "eligibility": "Farmers can contact their local soil testing facility.",
        "link": "https://soilhealth.dac.gov.in/",
        "icon": "🧪"
    },
    {
        "name": "Kisan Credit Card",
        "category": "Agricultural Credit",
        "description": "Provides eligible farmers access to institutional "
                       "credit for agricultural and allied activities.",
        "benefits": "Helps meet eligible farming credit requirements.",
        "eligibility": "Subject to bank rules and scheme conditions.",
        "link": "https://www.myscheme.gov.in/",
        "icon": "🏦"
    },
    {
        "name": "Paramparagat Krishi Vikas Yojana",
        "category": "Organic Farming",
        "description": "Promotes organic farming through cluster-based "
                       "approaches and support for participating farmers.",
        "benefits": "Encourages organic practices and soil health.",
        "eligibility": "As per programme guidelines and state implementation.",
        "link": "https://www.myscheme.gov.in/",
        "icon": "🌱"
    },
    {
        "name": "National Mission on Natural Farming",
        "category": "Natural Farming",
        "description": "Encourages natural farming practices and reduces "
                       "dependence on purchased agricultural inputs.",
        "benefits": "Promotes sustainable and nature-based farming.",
        "eligibility": "Check current state-level programme guidelines.",
        "link": "https://agriwelfare.gov.in/",
        "icon": "🌿"
    },
    {
        "name": "Agriculture Infrastructure Fund",
        "category": "Infrastructure",
        "description": "Supports eligible post-harvest management and "
                       "community farming infrastructure projects.",
        "benefits": "Financing support for eligible infrastructure projects.",
        "eligibility": "Eligible beneficiaries and projects under AIF guidelines.",
        "link": "https://agriinfra.dac.gov.in/",
        "icon": "🏗️"
    }
]

# Search and filters
st.subheader("🔎 Find a Government Scheme")

search = st.text_input(
    "Search by scheme name or keyword",
    placeholder="Example: crop insurance, soil, irrigation..."
)

categories = ["All"] + sorted(set(s["category"] for s in schemes))

selected_category = st.selectbox(
    "Filter by Category",
    categories
)

filtered_schemes = []

for scheme in schemes:
    matches_search = (
        search.lower() in scheme["name"].lower()
        or search.lower() in scheme["description"].lower()
        or search.lower() in scheme["category"].lower()
    )

    matches_category = (
        selected_category == "All"
        or scheme["category"] == selected_category
    )

    if matches_search and matches_category:
        filtered_schemes.append(scheme)

st.divider()

st.subheader(f"📚 Available Schemes ({len(filtered_schemes)})")

if not filtered_schemes:
    st.warning("No schemes found. Try another search.")

for scheme in filtered_schemes:
    with st.container(border=True):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.subheader(f"{scheme['icon']} {scheme['name']}")
            st.caption(scheme["category"])

        with col2:
            st.markdown(
                f'<a href="{scheme["link"]}" target="_blank">'
                '<button style="background:#176B3A;color:white;'
                'border:0;padding:10px 14px;border-radius:8px;'
                'cursor:pointer;">Official Portal ↗</button></a>',
                unsafe_allow_html=True
            )

        st.write(scheme["description"])

        with st.expander("View Scheme Details"):
            st.markdown(f"**Key Benefits:** {scheme['benefits']}")
            st.markdown(f"**Eligibility:** {scheme['eligibility']}")

st.divider()

st.subheader("📢 Important Farmer Portals")

portal_col1, portal_col2 = st.columns(2)

with portal_col1:
    st.markdown(
        "[🌐 Ministry of Agriculture](https://agriwelfare.gov.in/)"
    )
    st.markdown(
        "[🌐 MyScheme – Government Schemes](https://www.myscheme.gov.in/)"
    )

with portal_col2:
    st.markdown(
        "[🌐 PM-KISAN Portal](https://pmkisan.gov.in/)"
    )
    st.markdown(
        "[🌐 PM Fasal Bima Portal](https://pmfby.gov.in/)"
    )

st.warning(
    "Note: This is an informational scheme directory, not a live "
    "government notification feed. Scheme rules, benefits, eligibility "
    "and application windows may change. Verify details on official portals."
)

st.caption("KRISHI SAARTHI | Your Trusted Partner in Smart Farming")

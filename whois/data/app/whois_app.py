import streamlit as st
import requests

st.set_page_config(page_title="Whois API Explorer", layout="wide")
st.title("🔍 Whois API Explorer")


# --- IMAGE FETCH HELPERS ---

def fetch_duckduckgo_image(name):
    """Try to fetch image via DuckDuckGo Instant Answer API."""
    try:
        res = requests.get("https://api.duckduckgo.com/", params={
            "q": name,
            "format": "json"
        })
        data = res.json()
        return data.get("Image", "")
    except Exception:
        return ""


def fetch_wikipedia_image(name):
    """Fallback to Wikipedia thumbnail."""
    try:
        res = requests.get("https://en.wikipedia.org/w/api.php", params={
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "piprop": "thumbnail",
            "pithumbsize": 400,
            "titles": name
        }).json()

        pages = res.get("query", {}).get("pages", {})
        for page in pages.values():
            if "thumbnail" in page:
                return page["thumbnail"]["source"]
        return ""
    except Exception:
        return ""


def fetch_person_image(name):
    """Get image from DuckDuckGo, fall back to Wikipedia."""
    return fetch_duckduckgo_image(name) or fetch_wikipedia_image(name)


# --- UI INPUT ---

query = st.text_input("Enter a name to search:", "Neil Armstrong")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a valid name.")
    else:
        try:
            # Local whois API request
            res = requests.get("http://localhost:3000/api/v1/whois", data=query)
            data = res.json()

            if not data.get("success"):
                st.error("API call failed.")
            else:
                results = data.get("response", {}).get("data", [])
                if not results:
                    st.info("No data found for that name.")
                else:
                    person = results[0]
                    name = person.get("name__string", query)
                    image_url = fetch_person_image(name)

                    # --- Layout in Columns ---
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if image_url:
                            st.image(image_url, width=250, caption=name)
                        else:
                            st.info("No image found.")

                    with col2:
                        st.subheader(name)
                        st.markdown(f"**Introduction:** {person.get('introduction__string', '')}")
                        st.markdown(f"**Bio:** {person.get('bio__string', '')}")

                        known_for = person.get("known_for__array", [])
                        if known_for:
                            st.markdown("**Known For:**")
                            for item in known_for:
                                st.write(f"• {item}")

                        quotes = person.get("famous_quotes__array", [])
                        if quotes:
                            st.markdown("**Famous Quotes:**")
                            for quote in quotes:
                                st.success(f"💬 “{quote}”")

        except Exception as e:
            st.error(f"Error: {str(e)}")


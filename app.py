import streamlit as st
import requests

st.set_page_config(page_title="API-Football Maç Botu", layout="centered")
st.title("⚽ API-Football Maç Botu")

API_KEY = "53b61b1afa4d6e3fbc027d6cbfd6a68e"
headers = {
    "x-apisports-key": API_KEY
}

@st.cache_data(show_spinner=True)
def fetch_matches():
    url = "https://v3.football.api-sports.io/fixtures?next=10"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error(f"API erişim hatası! HTTP Kodu: {response.status_code}")
        return []

    data = response.json()
    matches = []

    for match in data.get("response", []):
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        date = match["fixture"]["date"].split("T")[0]
        matches.append({
            "match": f"{home} vs {away}",
            "date": date
        })

    return matches

if st.button("⚡ Maçları Göster"):
    with st.spinner("Maçlar yükleniyor..."):
        results = fetch_matches()

    if results:
        st.success(f"{len(results)} maç bulundu:")
        for match in results:
            st.markdown(f"📅 `{match['date']}` — **{match['match']}**")
    else:
        st.warning("Hiç maç bulunamadı veya API erişimi başarısız.")
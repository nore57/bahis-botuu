import streamlit as st
import requests

st.set_page_config(page_title="API Futbol Tahmin Botu", layout="centered")
st.title("⚽ API-Football AI Tahmin Botu")
st.markdown("Tahmini oran: 1.65 - 1.85 | Kazanma ihtimali: %70+")

headers = {
    "x-apisports-key": "53b61b1afa4d6e3fbc027d6cbfd6a68e"
}

@st.cache_data(show_spinner=True)
def fetch_matches():
    url = "https://v3.football.api-sports.io/fixtures?next=20"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("API'ye erişilemedi. HTTP Kod: " + str(response.status_code))
        return []

    data = response.json()
    matches = []

    for match in data.get("response", []):
        try:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            odds_url = f"https://v3.football.api-sports.io/odds?fixture={match['fixture']['id']}"
            odds_res = requests.get(odds_url, headers=headers)
            odds_data = odds_res.json()

            if not odds_data.get("response"):
                continue

            # Sadece 1X2 bahis tipini alalım
            bookmaker = odds_data["response"][0]["bookmakers"][0]
            bets = bookmaker["bets"]
            for bet in bets:
                if bet["name"] == "Match Winner":
                    for value in bet["values"]:
                        if value["value"] == "Home":
                            odd = float(value["odd"])
                            if 1.65 <= odd <= 1.85:
                                matches.append({
                                    "match": f"{home} vs {away}",
                                    "prediction": "Ev Sahibi Kazanır",
                                    "odds": odd
                                })
        except Exception as e:
            continue

    return matches

if st.button("⚡ Tahminleri Getir"):
    with st.spinner("Yapay zekâ analiz ediyor..."):
        results = fetch_matches()

    if results:
        st.success(f"Toplam {len(results)} uygun maç bulundu.")
        for match in results:
            st.markdown(f"**Maç:** {match['match']}")
            st.markdown(f"👉 Tahmin: `{match['prediction']}`")
            st.markdown(f"💸 Oran: `{match['odds']}`")
            st.markdown("---")
    else:
        st.warning("Uygun maç bulunamadı ya da API'ye erişilemedi.")
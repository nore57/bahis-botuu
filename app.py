import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Futbol AI Tahmin Botu", layout="centered")
st.title("⚽ Futbol AI Tahmin Botu")
st.markdown("Tahmini oran: 1.65 - 1.85 | Kazanma ihtimali: %70+")

@st.cache_data(show_spinner=True)
def fetch_matches():
    url = "https://www.forebet.com/en/football-predictions?statstype=preview"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    st.text("HTTP durum kodu: " + str(response.status_code))  # Hata ayıklama için

    if response.status_code != 200:
        st.error("Siteye erişilemedi. HTTP Kod: " + str(response.status_code))
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.select(".rcnt .tr_0, .rcnt .tr_1")

    if not rows:
        st.warning("Sayfada maç verisi bulunamadı. HTML yapısı değişmiş olabilir.")
        return []

    matches = []
    for row in rows:
        try:
            home = row.select_one(".homeTeam") or row.select_one(".team_home")
            away = row.select_one(".awayTeam") or row.select_one(".team_away")
            teams = home.text.strip() + " vs " + away.text.strip()

            prediction = row.select_one(".ptext2")
            prediction = prediction.text.strip() if prediction else "Yok"

            odds_elem = row.select_one(".odds_1X2_cell span.odds_bg1") or row.select_one(".odds_1X2_cell span.odds_bg2")
            odds = float(odds_elem.text.strip()) if odds_elem else 0.0

            prob_elem = row.select_one(".prob2")
            probability = int(prob_elem.text.strip().replace("%", "")) if prob_elem else 0

            if 1.65 <= odds <= 1.85 and probability >= 70:
                matches.append({
                    "match": teams,
                    "prediction": prediction,
                    "odds": odds,
                    "win_chance": probability
                })
        except Exception as e:
            print("Hata:", e)
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
            st.markdown(f"📈 Kazanma Şansı: `%{match['win_chance']}`")
            st.markdown("---")
    else:
        st.warning("Uygun maç bulunamadı ya da siteye erişilemedi.")
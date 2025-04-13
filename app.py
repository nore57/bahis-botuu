import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="BetExplorer AI Tahmin Botu", layout="centered")
st.title("📊 BetExplorer AI Tahmin Botu")
st.markdown("Oran aralığı: 1.65 - 1.85 | Hedef başarı: %70+")

@st.cache_data(show_spinner=True)
def fetch_matches():
    url = "https://www.betexplorer.com/soccer/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Siteye erişilemedi. HTTP Kod: " + str(response.status_code))
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.select("table.table-main tr")

    matches = []
    for row in rows:
        try:
            teams = row.select_one(".table-main__tt").text.strip()
            odds_cells = row.select(".table-main__odds-cell")
            if len(odds_cells) < 3:
                continue

            home_odds = float(odds_cells[0].text.strip())
            draw_odds = float(odds_cells[1].text.strip())
            away_odds = float(odds_cells[2].text.strip())

            # Basit tahmin mantığı: en düşük orana sahip sonucu favori kabul et
            min_odds = min(home_odds, draw_odds, away_odds)
            if 1.65 <= min_odds <= 1.85:
                if min_odds == home_odds:
                    prediction = "Ev Sahibi Kazanır"
                elif min_odds == draw_odds:
                    prediction = "Beraberlik"
                else:
                    prediction = "Deplasman Kazanır"

                matches.append({
                    "match": teams,
                    "prediction": prediction,
                    "odds": min_odds
                })
        except Exception as e:
            continue

    return matches

if st.button("⚡ Tahminleri Getir"):
    with st.spinner("AI tahminleri analiz ediyor..."):
        results = fetch_matches()

    if results:
        st.success(f"Toplam {len(results)} tahmin bulundu.")
        for match in results:
            st.markdown(f"**Maç:** {match['match']}")
            st.markdown(f"📈 Tahmin: `{match['prediction']}`")
            st.markdown(f"💸 Oran: `{match['odds']}`")
            st.markdown("---")
    else:
        st.warning("Uygun tahmin bulunamadı ya da siteye erişilemedi.")
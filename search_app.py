import streamlit as st
from duckduckgo_search import DDGS
from datetime import datetime
import hashlib

# ---------- APP-KONFIGURATION ----------
st.set_page_config(
    page_title="🌐 Smart Web Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS FÜR IPHONE-OPTIMIERUNG ----------
st.markdown("""
<style>
    /* Größere Buttons für Touch */
    .stButton > button {
        width: 100%;
        padding: 0.75rem !important;
        font-size: 1.2rem !important;
        border-radius: 12px !important;
    }
    /* Kartendesign für Ergebnisse */
    .result-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 4px solid #ff4b4b;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .result-card img {
        border-radius: 8px;
        max-width: 100%;
        height: auto;
    }
    /* Titel in Karten */
    .result-card h3 {
        margin-top: 0;
        color: #1e1e1e;
    }
    .result-card a {
        color: #0066cc;
        text-decoration: none;
        word-break: break-all;
    }
    /* Abstand für Mobilansicht */
    @media (max-width: 600px) {
        .result-card {
            padding: 12px;
        }
        .stTextInput > div > div > input {
            font-size: 16px !important;
            padding: 12px !important;
        }
    }
    /* Fortschrittsbalken */
    .stProgress > div > div {
        background-color: #ff4b4b !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR: FILTER ----------
with st.sidebar:
    st.header("⚙️ Filter")
    
    search_type = st.selectbox(
        "📂 Inhaltstyp",
        ["Web", "Bilder", "News", "Videos"],
        help="Wähle, was du finden möchtest."
    )
    
    region = st.selectbox(
        "🌍 Region",
        ["wt-wt", "de-de", "us-en", "uk-en", "fr-fr", "es-es", "it-it", "jp-jp"],
        format_func=lambda x: {
            "wt-wt": "🌍 Weltweit",
            "de-de": "🇩🇪 Deutschland",
            "us-en": "🇺🇸 USA",
            "uk-en": "🇬🇧 Großbritannien",
            "fr-fr": "🇫🇷 Frankreich",
            "es-es": "🇪🇸 Spanien",
            "it-it": "🇮🇹 Italien",
            "jp-jp": "🇯🇵 Japan"
        }.get(x, x)
    )
    
    time_filter = st.selectbox(
        "⏱️ Zeitraum",
        ["Jederzeit", "Tag", "Woche", "Monat", "Jahr"],
        help="Zeigt nur Ergebnisse aus dem gewählten Zeitraum."
    )
    
    max_results = st.slider("📊 Max. Ergebnisse", 5, 50, 25)
    
    st.divider()
    st.caption("💡 **Tipp:** Doppelte Einträge werden automatisch entfernt.")

# ---------- HAUPTBEREICH: SUCHLEISTE ----------
st.title("🔍 Smart Web Search")
st.caption("Durchsucht das gesamte WWW, filtert Duplikate & sammelt alle Infos")

query = st.text_input(
    "✏️ Suchbegriff eingeben",
    placeholder="z.B. Künstliche Intelligenz, iPhone 16, Klimawandel...",
    label_visibility="collapsed"
)

# Zeitfilter umwandeln
time_map = {
    "Jederzeit": None,
    "Tag": "d",
    "Woche": "w",
    "Monat": "m",
    "Jahr": "y"
}

# ---------- DUPLIKAT-FILTER-FUNKTION ----------
def remove_duplicates(results, key_fields):
    """Entfernt Duplikate basierend auf einem generierten Hash aus key_fields"""
    seen = set()
    unique = []
    
    for item in results:
        # Generiere einen eindeutigen Schlüssel aus Titel + URL (oder Bild-URL)
        hash_input = ""
        for field in key_fields:
            hash_input += str(item.get(field, ""))
        
        # Bei Bildern: URL als Fallback
        if not hash_input.strip():
            hash_input = str(item.get("image", "")) + str(item.get("thumbnail", ""))
        
        item_hash = hashlib.md5(hash_input.encode('utf-8')).hexdigest()
        
        if item_hash not in seen:
            seen.add(item_hash)
            unique.append(item)
    
    return unique

# ---------- SUCHLOGIK ----------
if st.button("🚀 Los suchen", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("⚠️ Bitte gib einen Suchbegriff ein.")
    else:
        with st.spinner(f"🔎 Durchsuche das Web nach ‚{query}‘..."):
            try:
                ddgs = DDGS()
                results = []
                t_limit = time_map[time_filter]
                reg = region
                
                # Fortschrittsanzeige
                progress_bar = st.progress(0, text="Verbinde mit DuckDuckGo...")
                
                # Je nach Typ die passende DDGS-Methode
                if search_type == "Web":
                    progress_bar.progress(30, text="Durchsuche Webseiten...")
                    results = list(ddgs.text(query, region=reg, timelimit=t_limit, max_results=max_results))
                    # Duplikate entfernen basierend auf Titel + URL
                    results = remove_duplicates(results, ["title", "href"])
                
                elif search_type == "Bilder":
                    progress_bar.progress(30, text="Durchsuche Bilder...")
                    results = list(ddgs.images(query, region=reg, timelimit=t_limit, max_results=max_results))
                    results = remove_duplicates(results, ["title", "image"])
                
                elif search_type == "News":
                    progress_bar.progress(30, text="Durchsuche News...")
                    results = list(ddgs.news(query, region=reg, timelimit=t_limit, max_results=max_results))
                    results = remove_duplicates(results, ["title", "url"])
                
                elif search_type == "Videos":
                    progress_bar.progress(30, text="Durchsuche Videos...")
                    results = list(ddgs.videos(query, region=reg, timelimit=t_limit, max_results=max_results))
                    results = remove_duplicates(results, ["title", "content"])
                
                progress_bar.progress(100, text="Fertig!")
                
                # ---------- ERGEBNISSE ANZEIGEN ----------
                if not results:
                    st.info("😕 Keine Ergebnisse gefunden. Versuche andere Begriffe oder Filter.")
                else:
                    st.success(f"✅ **{len(results)}** einzigartige Ergebnisse gefunden (Duplikate entfernt!)")
                    
                    # Ergebnisse als Karten darstellen
                    for idx, item in enumerate(results):
                        with st.container(border=True):
                            if search_type in ["Web", "News"]:
                                title = item.get('title', 'Ohne Titel')
                                link = item.get('href', '#')
                                body = item.get('body', 'Keine Beschreibung')
                                st.markdown(f"### [{title}]({link})")
                                st.write(body[:600] + "..." if len(body) > 600 else body)
                                if search_type == "News" and item.get('date'):
                                    st.caption(f"📅 {item['date']}")
                                st.caption(f"🔗 [Quelle öffnen]({link})")
                            
                            elif search_type == "Bilder":
                                cols = st.columns([1, 2])
                                with cols[0]:
                                    img_url = item.get('image', '')
                                    if img_url:
                                        st.image(img_url, width=150, use_container_width=False)
                                    else:
                                        st.write("🖼️ (kein Bild)")
                                with cols[1]:
                                    st.markdown(f"**{item.get('title', 'Bild')}**")
                                    if item.get('source'):
                                        st.caption(f"📷 Quelle: {item['source']}")
                                    if item.get('dimensions'):
                                        st.caption(f"📐 {item['dimensions']}")
                            
                            elif search_type == "Videos":
                                video_url = item.get('content') or item.get('embed_url')
                                if video_url:
                                    # Prüfen ob Embed möglich
                                    if "youtube.com" in video_url or "youtu.be" in video_url:
                                        st.video(video_url)
                                    else:
                                        st.write(f"🔗 [Video ansehen]({video_url})")
                                else:
                                    if item.get('thumbnail'):
                                        st.image(item.get('thumbnail'), width=200)
                                st.markdown(f"**{item.get('title', 'Video')}**")
                                if item.get('description'):
                                    st.write(item['description'][:300])
                                if item.get('duration'):
                                    st.caption(f"⏱️ Dauer: {item['duration']}")
                            
                            # Kleine Info über Duplikat-Entfernung
                            st.caption(f"📌 Ergebnis #{idx+1} von {len(results)}")
                
                # Lösche Fortschrittsbalken nach Ergebnisanzeige
                progress_bar.empty()
                
            except Exception as e:
                st.error(f"🚨 **Fehler:** {e}")
                st.info("🔄 Tipp: Warte 1-2 Minuten und versuche es erneut. Bei häufigen Fehlern kann DuckDuckGo kurzfristig blockieren.")

# ---------- FOOTER ----------
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🔍 Powered by DuckDuckGo")
with col2:
    st.caption("🧹 Duplikate automatisch gefiltert")
with col3:
    st.caption("📱 Optimiert für iPhone")

# Tipp für Home-Screen
st.info("💡 **Tipp:** Füge diese App zum iPhone-Home-Bildschirm hinzu: \n\n"
        "1. Tippe auf das **Teilen-Symbol** (📤) im Safari\n"
        "2. Wähle **„Zum Home-Bildschirm“**\n"
        "3. Tippe auf **„Hinzufügen“** – die App startet dann wie eine native App!")

import streamlit as st
from duckduckgo_search import DDGS
import hashlib
import re
from collections import Counter

# ---------- APP-KONFIGURATION ----------
st.set_page_config(
    page_title="📚 Smart Research Assistant",
    page_icon="📖",
    layout="wide"
)

# ---------- CSS FÜR BESSERE DARSTELLUNG ----------
st.markdown("""
<style>
    .big-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 20px;
        color: white;
        margin-bottom: 20px;
    }
    .info-box {
        background: #f0f2f6;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border-left: 4px solid #ff4b4b;
    }
    .tag {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 4px;
    }
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #ff4b4b;
    }
    .result-item {
        background: white;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        border: 1px solid #e0e0e0;
    }
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 10px;
        margin: 10px 0;
    }
    .image-grid img {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("⚙️ Einstellungen")
    max_web = st.slider("🌐 Webseiten", 5, 30, 15)
    max_images = st.slider("🖼️ Bilder", 5, 30, 10)
    max_news = st.slider("📰 News", 5, 20, 8)
    max_videos = st.slider("🎬 Videos", 3, 15, 5)

# ---------- HAUPTBEREICH ----------
st.title("📚 Smart Research Assistant")
st.markdown("""
<div class="big-card">
    <h2 style="margin:0;">🔍 Gib einen Begriff ein – ich sammle alles!</h2>
</div>
""", unsafe_allow_html=True)

query = st.text_input("✏️ Suchbegriff", placeholder="z.B. Maya, KI, Klimawandel...")

# ---------- HILFSFUNKTIONEN ----------
def extract_keywords(text, top_n=10):
    words = re.findall(r'\b[a-zA-ZäöüßÄÖÜ]{3,}\b', text.lower())
    stopwords = {'und', 'der', 'die', 'das', 'den', 'mit', 'von', 'für', 'ist', 'im', 'dem', 'des', 'auf', 'bei', 'ein', 'eine', 'einen', 'einer', 'als', 'auch', 'nur', 'zur', 'aus'}
    words = [w for w in words if w not in stopwords]
    return Counter(words).most_common(top_n)

def remove_duplicates(results, key_fields):
    seen = set()
    unique = []
    for item in results:
        hash_input = "".join(str(item.get(field, "")) for field in key_fields)
        item_hash = hashlib.md5(hash_input.encode('utf-8')).hexdigest()
        if item_hash not in seen:
            seen.add(item_hash)
            unique.append(item)
    return unique

# ---------- SUCHLOGIK ----------
if st.button("🚀 Recherche starten", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("⚠️ Bitte gib einen Suchbegriff ein.")
    else:
        st.markdown(f"## 📊 Ergebnisse für: **{query}**")
        
        with st.spinner(f"🔎 Durchsuche das Web nach ‚{query}‘..."):
            try:
                ddgs = DDGS()
                web_results = []
                image_results = []
                news_results = []
                video_results = []
                
                progress = st.progress(0)
                
                # 1. Web
                progress.progress(10, text="Durchsuche Webseiten...")
                try:
                    web_results = list(ddgs.text(query, max_results=max_web))
                    web_results = remove_duplicates(web_results, ["title", "href"])
                except:
                    pass
                
                # 2. Bilder
                progress.progress(30, text="Sammle Bilder...")
                try:
                    image_results = list(ddgs.images(query, max_results=max_images))
                    image_results = remove_duplicates(image_results, ["title", "image"])
                except:
                    pass
                
                # 3. News
                progress.progress(60, text="Sammle News...")
                try:
                    news_results = list(ddgs.news(query, max_results=max_news))
                    news_results = remove_duplicates(news_results, ["title", "url"])
                except:
                    pass
                
                # 4. Videos
                progress.progress(80, text="Sammle Videos...")
                try:
                    video_results = list(ddgs.videos(query, max_results=max_videos))
                    video_results = remove_duplicates(video_results, ["title", "content"])
                except:
                    pass
                
                progress.progress(100, text="Fertig!")
                
                total = len(web_results) + len(image_results) + len(news_results) + len(video_results)
                
                if total == 0:
                    st.info("😕 Keine Ergebnisse gefunden.")
                else:
                    # Statistik
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-number">{len(web_results)}</div>
                            <div>🌐 Webseiten</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-number">{len(image_results)}</div>
                            <div>🖼️ Bilder</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-number">{len(news_results)}</div>
                            <div>📰 News</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-number">{len(video_results)}</div>
                            <div>🎬 Videos</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # ---------- SCHLAGWÖRTER ----------
                    all_text = ""
                    for item in web_results[:5]:
                        all_text += item.get("title", "") + " " + item.get("body", "") + " "
                    for item in news_results[:5]:
                        all_text += item.get("title", "") + " " + item.get("body", "") + " "
                    
                    if all_text:
                        keywords = extract_keywords(all_text, 8)
                        if keywords:
                            st.markdown("### 🏷️ Wichtigste Schlagwörter")
                            tags = " ".join([f'<span class="tag">{word} ({count})</span>' for word, count in keywords])
                            st.markdown(tags, unsafe_allow_html=True)
                            st.divider()
                    
                    # ---------- BILDER ----------
                    if image_results:
                        st.markdown("### 🖼️ Bilder")
                        cols = st.columns(4)
                        for idx, img in enumerate(image_results[:8]):
                            with cols[idx % 4]:
                                if img.get('image'):
                                    st.image(img['image'], use_container_width=True)
                                    st.caption(img.get('title', '')[:30])
                        st.divider()
                    
                    # ---------- WEBSEITEN ----------
                    if web_results:
                        st.markdown("### 🌐 Webseiten")
                        for item in web_results[:5]:
                            title = item.get('title', 'Ohne Titel')
                            link = item.get('href', '#')
                            body = item.get('body', 'Keine Beschreibung')
                            st.markdown(f"""
                            <div class="result-item">
                                <strong><a href="{link}" target="_blank">{title}</a></strong>
                                <br><small>{body[:200]}{"..." if len(body) > 200 else ""}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        st.divider()
                    
                    # ---------- NEWS ----------
                    if news_results:
                        st.markdown("### 📰 News")
                        for item in news_results[:3]:
                            title = item.get('title', 'Ohne Titel')
                            link = item.get('url', '#')
                            body = item.get('body', '')
                            date = item.get('date', '')
                            st.markdown(f"""
                            <div class="result-item">
                                <strong><a href="{link}" target="_blank">{title}</a></strong>
                                {" 📅 " + date if date else ""}
                                <br><small>{body[:150]}{"..." if len(body) > 150 else ""}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        st.divider()
                    
                    # ---------- VIDEOS ----------
                    if video_results:
                        st.markdown("### 🎬 Videos")
                        for item in video_results[:3]:
                            title = item.get('title', 'Video')
                            video_url = item.get('content') or item.get('embed_url')
                            if video_url and "youtube.com" in video_url:
                                st.video(video_url)
                                st.caption(title)
                            elif video_url:
                                st.markdown(f"[▶️ {title}]({video_url})")
                    
                    progress.empty()
                    
            except Exception as e:
                st.error(f"🚨 Fehler: {e}")

# ---------- FOOTER ----------
st.divider()
st.caption("📱 Optimiert für iPhone | 🔍 Durchsucht das gesamte Web | 🧹 Doppelte Inhalte gefiltert")

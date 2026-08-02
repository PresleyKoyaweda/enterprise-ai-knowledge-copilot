import requests
import streamlit as st

API_BASE_URL = "https://enterprise-ai-copilot-api.onrender.com/api/v1"

st.set_page_config(
    page_title="Conforma — Agent Loi 25",
    page_icon="◆",
    layout="centered",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container { max-width: 720px; padding-top: 2.5rem; }

.brand-mark {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    border: 1.5px solid #C9A66B;
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.3rem;
    color: #C9A66B;
    margin-bottom: 1.1rem;
}

.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #C9A66B;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.5rem;
    line-height: 1.1;
    color: #F0EDE6;
    margin-bottom: 0.7rem;
    letter-spacing: -0.015em;
}
.hero-title span { color: #C9A66B; }
.hero-tagline {
    font-size: 1.02rem;
    color: #93A0BD;
    line-height: 1.6;
    max-width: 560px;
    margin-bottom: 2rem;
}

/* -- About panel -- */
.about-panel {
    border: 1px solid #2A3655;
    border-radius: 8px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 2.2rem;
    background: linear-gradient(180deg, #131D34 0%, #0E1526 100%);
}
.about-row {
    display: flex;
    gap: 1.4rem;
    padding: 0.85rem 0;
}
.about-row + .about-row { border-top: 1px solid #202B48; }
.about-key {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #C9A66B;
    width: 130px;
    flex-shrink: 0;
    padding-top: 0.15rem;
}
.about-value {
    font-size: 0.92rem;
    color: #D7DCE8;
    line-height: 1.55;
}

.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #93A0BD;
    margin-bottom: 0.9rem;
}

[data-testid="stChatMessage"] {
    background-color: #16203A;
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    border: 1px solid #2A3655;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 3px solid #C9A66B;
}
[data-testid="stChatInput"] textarea {
    background-color: #16203A !important;
    border: 1px solid #2A3655 !important;
    color: #F0EDE6 !important;
}

.citation-card {
    background-color: #0E1526;
    border: 1px solid #2A3655;
    border-left: 3px solid #C9A66B;
    border-radius: 4px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.6rem;
}
.citation-card .citation-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #C9A66B;
    margin-bottom: 0.3rem;
}
.citation-card .citation-excerpt {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 0.9rem;
    color: #93A0BD;
    line-height: 1.5;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="brand-mark">C.</div>
    <div class="hero-eyebrow">Legaltech — Conformité québécoise</div>
    <div class="hero-title">Conforma<span>.</span><br>La Loi 25, sans le jargon.</div>
    <p class="hero-tagline">
        Un agent d'intelligence artificielle spécialisé, conçu pour répondre en langage clair
        aux questions de conformité que se posent réellement les entreprises québécoises —
        sources officielles citées à chaque réponse.
    </p>

    <div class="about-panel">
        <div class="about-row">
            <div class="about-key">Contexte</div>
            <div class="about-value">
                Depuis l'entrée en vigueur complète de la Loi 25 en 2023, toute organisation qui
                traite des renseignements personnels au Québec est soumise à des obligations
                strictes de conformité, de transparence et de gouvernance des données.
            </div>
        </div>
        <div class="about-row">
            <div class="about-key">Thématique</div>
            <div class="about-value">
                Protection des renseignements personnels et conformité juridique — Loi
                modernisant des dispositions législatives en matière de protection des
                renseignements personnels (Québec).
            </div>
        </div>
        <div class="about-row">
            <div class="about-key">Objectif</div>
            <div class="about-value">
                Rendre la conformité accessible : traduire un texte de loi dense en réponses
                concrètes, applicables, et toujours appuyées sur les documents officiels
                consultés.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_sources(sources: list[dict]) -> None:
    if not sources:
        return
    with st.expander(f"§ {len(sources)} source(s) citée(s)"):
        for source in sources:
            st.markdown(
                f"""
                <div class="citation-card">
                    <div class="citation-header">{source['document_name']} — pertinence {source['score']:.2f}</div>
                    <div class="citation-excerpt">« {source['excerpt']} »</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def process_question(question: str) -> None:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultation des documents en cours... (jusqu'à 60 secondes au premier appel)"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={"question": question},
                    timeout=90,
                )
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                sources = data.get("sources", [])

                st.markdown(answer)
                render_sources(sources)

            except requests.exceptions.RequestException as error:
                answer = f"L'agent est momentanément injoignable. Détail : {error}"
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


st.markdown('<div class="section-label">Poser une question</div>', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Posez votre question sur la Loi 25..."):
    process_question(question)
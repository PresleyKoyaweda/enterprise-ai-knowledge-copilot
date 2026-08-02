import requests
import streamlit as st

API_BASE_URL = "https://enterprise-ai-copilot-api.onrender.com/api/v1"

st.set_page_config(
    page_title="Agent Loi 25 — Québec",
    page_icon="⚖️",
    layout="centered",
)

st.title("⚖️ Agent Loi 25 — Québec")
st.caption(
    "Posez vos questions sur la protection des renseignements personnels au Québec. "
    "Les réponses sont générées à partir de documents officiels, avec citation des sources."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Posez votre question sur la Loi 25..."):
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours... (le premier appel peut prendre jusqu'à 60 secondes)"):
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

                if sources:
                    with st.expander(f"📄 {len(sources)} source(s) citée(s)"):
                        for source in sources:
                            st.markdown(f"**{source['document_name']}** (pertinence : {source['score']:.2f})")
                            st.caption(source["excerpt"])

            except requests.exceptions.RequestException as error:
                answer = f"Erreur de connexion à l'agent : {error}"
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
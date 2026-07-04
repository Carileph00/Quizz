import streamlit as st
import json
from google import genai

st.title("🧠 Quiz Interactif Expert")

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

theme = st.text_input("Saisissez votre thème :")

if st.button("Générer le Quiz Interactif"):
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    prompt = f"""
    Génère 5 questions de QCM sur {theme}. 
    Réponds EXCLUSIVEMENT au format JSON comme ceci :
    [
        {{"question": "...", "options": ["A", "B", "C", "D"], "reponse": "A", "explication": "..."}}
    ]
    """
    
    reponse = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    st.session_state.quiz_data = json.loads(reponse.text.replace("```json", "").replace("```", ""))

# Affichage du quiz interactif
if st.session_state.quiz_data:
    for i, item in enumerate(st.session_state.quiz_data):
        st.subheader(f"Q{i+1}: {item['question']}")
        
        # On crée un groupe de boutons pour chaque question
        choix = st.radio(f"Réponse {i+1}", item['options'], key=f"q{i}")
        
        if st.button(f"Valider Q{i+1}", key=f"btn{i}"):
            if choix == item['reponse']:
                st.success("Correct !")
            else:
                st.error(f"Faux. La bonne réponse était : {item['reponse']}")
            st.info(item['explication'])

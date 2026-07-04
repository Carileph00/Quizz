import streamlit as st
import json
from google import genai

st.title("🧠 Quiz Interactif Expert")

# Initialisation de la mémoire pour garder les questions et les résultats affichés
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "reponses_donnees" not in st.session_state:
    st.session_state.reponses_donnees = {}

theme = st.text_input("Saisissez votre thème :")

if st.button("Générer les 20 questions"):
    
    if theme:
        # On réinitialise la mémoire à chaque nouveau quiz
        st.session_state.quiz_data = None
        st.session_state.reponses_donnees = {}
        
        with st.spinner("Création du quiz en cours (cela peut prendre environ 15 secondes)..."):
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                                # Le prompt repensé avec la contrainte stricte de langue
                prompt = f"""
                Agis comme un créateur de quiz expert. 
                Génère 20 questions de QCM EN FRANÇAIS sur le thème : {theme}. 
                Contraintes IMPÉRATIVES :
                1. Difficulté strictement croissante (1 = facile, 20 = expert).
                2. Ne mets AUCUNE lettre (A, B, C, D) devant les choix de réponses.
                3. La valeur "reponse" DOIT être strictement identique au texte de la bonne option.
                4. TOUT le contenu généré (questions, options, reponse et explication) DOIT OBLIGATOIREMENT être rédigé en français.
                
                Réponds EXCLUSIVEMENT au format JSON strict comme cet exemple :
                [
                    {{
                        "question": "Quel est l'animal de compagnie de Toriko ?", 
                        "options": ["Terry Cloth", "Kiss", "Quinn", "Kruk"], 
                        "reponse": "Terry Cloth", 
                        "explication": "Terry est un Loup de Bataille cloné..."
                    }}
                ]
                """

                
                reponse = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                
                # Nettoyage du texte généré pour extraire le JSON pur
                texte_json = reponse.text.replace("```json", "").replace("```", "").strip()
                st.session_state.quiz_data = json.loads(texte_json)
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de la génération : {e}")
    else:
        st.warning("Veuillez entrer un thème.")

# Affichage du quiz interactif
if st.session_state.quiz_data:
    st.success("Quiz généré ! À vous de jouer.")
    
    for i, item in enumerate(st.session_state.quiz_data):
        st.markdown(f"### Q{i+1} : {item['question']}")
        
        # Création des vraies cases cliquables
        for j, option in enumerate(item['options']):
            if st.button(option, key=f"btn_{i}_{j}"):
                # Enregistrement du résultat en mémoire lors du clic
                if option == item['reponse']:
                    st.session_state.reponses_donnees[i] = {
                        "status": "success", 
                        "msg": "✅ Correct !", 
                        "exp": item['explication']
                    }
                else:
                    st.session_state.reponses_donnees[i] = {
                        "status": "error", 
                        "msg": f"❌ Faux. La bonne réponse était : {item['reponse']}", 
                        "exp": item['explication']
                    }
        
        # Affichage du résultat de la question sous les boutons
        if i in st.session_state.reponses_donnees:
            res = st.session_state.reponses_donnees[i]
            if res["status"] == "success":
                st.success(res["msg"])
            else:
                st.error(res["msg"])
            st.info(res["exp"])
            
        # Ligne de séparation pour rendre la lecture plus aérée sur téléphone
        st.divider() 

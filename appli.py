import streamlit as st
import json
from google import genai

st.title("Quipro-Quizz")

# Initialisation de la mémoire
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "reponses_donnees" not in st.session_state:
    st.session_state.reponses_donnees = {}

theme = st.text_input("Saisissez votre thème :")

if st.button("Générer les 20 questions"):
    if theme:
        st.session_state.quiz_data = None
        st.session_state.reponses_donnees = {}
        with st.spinner("Génération du quiz en cours..."):
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                # Prompt optimisé pour la précision des noms et le format
                prompt = f"""
                Agis comme un expert passionné et créateur de quiz.
                Génère 20 questions de QCM sur le thème : {theme}.
                
                Contraintes STRICTES :
                1. Utilise les NOMS OFFICIELS FRANÇAIS (localisés) des œuvres/jeux. Ne fais pas de traduction littérale (ex: 'Sanctuaire de Lige-Feu' et non 'Autel du lien').
                2. Base tes questions sur des faits vérifiés (wikis officiels).
                3. Difficulté croissante (1 = facile, 20 = expert).
                4. Ne mets AUCUNE lettre (A, B, C, D) dans les options.
                5. La valeur 'reponse' doit être strictement identique au texte de l'option choisie.
                6. Tout le contenu doit être rédigé en FRANÇAIS.

                Réponds UNIQUEMENT en JSON pur :
                [
                    {{"question": "...", "options": ["...", "...", "...", "..."], "reponse": "...", "explication": "..."}}
                ]
                """
                
                reponse = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                
                # Extraction sécurisée du JSON
                texte = reponse.text
                debut = texte.find('[')
                fin = texte.rfind(']') + 1
                
                if debut != -1 and fin != 0:
                    st.session_state.quiz_data = json.loads(texte[debut:fin])
                else:
                    st.error("L'IA n'a pas respecté le format demandé. Réessaie.")
                    
            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
    else:
        st.warning("Veuillez entrer un thème.")

# Affichage et gestion des clics
if st.session_state.quiz_data:
    st.success("Quiz prêt !")
    for i, item in enumerate(st.session_state.quiz_data):
        st.markdown(f"### Q{i+1} : {item['question']}")
        
        for option in item['options']:
            if st.button(option, key=f"btn_{i}_{option}"):
                if option == item['reponse']:
                    st.session_state.reponses_donnees[i] = {
                        "status": "success", 
                        "msg": "✅ Correct !", 
                        "exp": item['explication']
                    }
                else:
                    st.session_state.reponses_donnees[i] = {
                        "status": "error", 
                        "msg": f"❌ Faux. Réponse : {item['reponse']}", 
                        "exp": item['explication']
                    }
        
        # Affichage du résultat si déjà répondu
        if i in st.session_state.reponses_donnees:
            res = st.session_state.reponses_donnees[i]
            if res["status"] == "success":
                st.success(res["msg"])
            else:
                st.error(res["msg"])
            st.info(res["exp"])
        st.divider()

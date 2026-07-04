import streamlit as st
from google import genai  # Utilisation de la nouvelle bibliothèque officielle 2026

# --- CONFIGURATION DE L'INTERFACE ---
st.title("🧠 Générateur de Quiz Expert")
st.write("Saisissez un thème pour générer 10 questions de difficulté croissante.")

# Barre de recherche
theme_quiz = st.text_input("Votre thème (ex: Le fromage Maroilles, le manga Toriko...) :")

# Bouton pour lancer la génération
if st.button("Générer le Quiz"):
    
    if theme_quiz:
        # Animation de chargement
        with st.spinner("Création de votre quiz en cours..."):
            
            try:
                # Nouvelle méthode d'initialisation propre à 2026
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                prompt = f"""
                Agis comme un créateur de quiz expert. 
                Génère 10 questions sur le thème suivant : {theme_quiz}.
                Contraintes :
                1. Difficulté strictement croissante (1 = facile, 10 = expert).
                2. Fournis la réponse correcte.
                3. Ajoute une courte explication précise pour chaque réponse.
                """
                
                # Nouvelle syntaxe pour générer le contenu
                reponse = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                # --- AFFICHAGE DU RÉSULTAT ---
                st.success("Quiz généré avec succès !")
                st.markdown(reponse.text)
                
            except Exception as e:
                st.error(f"Une erreur est survenue avec l'API : {e}")
            
    else:
        st.warning("Veuillez entrer un thème avant de générer le quiz.")

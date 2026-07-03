import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE L'INTERFACE ---
st.title("🧠 Générateur de Quiz Expert")
st.write("Saisissez un thème pour générer 20 questions de difficulté croissante.")

# Barre de recherche
theme_quiz = st.text_input("Votre thème (ex: Le fromage Maroilles, le manga Toriko...) :")

# Bouton pour lancer la génération
if st.button("Générer le Quiz"):
    
    if theme_quiz:
        # Animation de chargement pendant que l'IA travaille
        with st.spinner("Recherche des sources et création du quiz (cela prend environ 15 secondes)..."):
            
            # --- LE MOTEUR IA ---
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Agis comme un créateur de quiz expert. 
            Génère 20 questions sur le thème suivant : {theme_quiz}.
            Contraintes :
            1. Difficulté strictement croissante (1 = facile, 20 = expert).
            2. Fournis la réponse correcte.
            3. Vérifie via le web et ajoute une courte explication sourcée pour chaque réponse.
            """
            
            # Requête à Gemini avec la recherche Google activée
            reponse = model.generate_content(
                prompt,
                tools=['google_search']
            )
            
            # --- AFFICHAGE DU RÉSULTAT ---
            st.success("Quiz généré avec succès !")
            st.markdown(reponse.text)
            
    else:
        st.warning("Veuillez entrer un thème avant de générer le quiz.")

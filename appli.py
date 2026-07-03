import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE L'INTERFACE ---
# Titre de l'application
st.title("🧠 Générateur de Quiz Expert")
st.write("Saisissez un thème pour générer 20 questions de difficulté croissante.")

# Barre de recherche pour que tu puisses taper ton thème
theme_quiz = st.text_input("Votre thème (ex: Le fromage Maroilles, le manga Toriko...) :")

# Bouton pour lancer la génération
if st.button("Générer le Quiz"):
    
    # Vérification que le champ n'est pas vide
    if theme_quiz:
        # st.spinner affiche une animation de chargement pendant que l'IA cherche
        with st.spinner("Recherche des sources et création du quiz (cela prend environ 15 secondes)..."):
            
            # --- LE MOTEUR IA ---
            model = genai.GenerativeModel('gemini-1.5-flash')

# ... plus bas ...

reponse = model.generate_content(
    prompt,
    tools=['google_search'] # La nouvelle syntaxe simplifiée
)

            
            # --- AFFICHAGE DU RÉSULTAT ---
            st.success("Quiz généré avec succès !")
            # st.markdown permet d'afficher le texte avec un beau formatage (gras, listes, etc.)
            st.markdown(reponse.text)
    else:
        st.warning("Veuillez entrer un thème avant de générer le quiz.")

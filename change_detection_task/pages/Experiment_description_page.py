import streamlit as st
import random
from core.scripts import user_repository

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

css = """
.st-key-my_blue_container {
    background-color: rgba(100, 100, 200, 0.3);
}
"""

st.html(f"<style>{css}</style>")

st.html("<h1 style='text-align: center;'>Teste dein Gedächtnis!</h1><h3 style='text-align: center;'>In diesem Experiment, kannst du dein Gedächtnis mit dem eines großen Sprachmodels (LLM) messen.</h3")


st.html("<p><b><i>Was ist ein LLM?</i></b></p> <p>Bei LLMs handelt es sich um KI-Modelle wie ChatGPT, die auf riesigen Textmengen trainiert wurden, um Texte zu generieren und verstehen.</p>")
st.html("<p><b><i>Und wie ist das mit dem Gedächtnis gemeint?</i></b></p> <p>LLMs haben ein sogenanntes Context-Window. Das beschreibt die Menge an Text, die sie innerhalb einer Interaktion oder Unterhaltung miteinbeziehen können. Es ist also so etwas wie das \"Kurzzeitgedächtnis\" von LLMs.</p><p>Aber LLMs können beim Abruf von Informationen Fehler machen, selbst wenn sie innerhalb des Context-Windows liegen. Das kann zum Beispiel passieren, wenn eine Interaktion länger dauert und somit mehr Inhalt im \"Kurzzeitgedächtnis\" des LLMs gespeichert werden muss.</p>")
with st.container(border=False, key="my_blue_container"):
        st.html("""<p><b><i>Wie funktioniert das Experiment?</i></b></p><p>Im Folgenden wirst du 6 Nachrichtenüberschriften sehen, die du dir so gut wie möglich einprägen sollst. Im Anschluss wird deine Erinnerung getestet.</p>
                <p>Die KI hat die gleichen Überschriften gesehen, allerdings wurde ihr danach auch noch eine Sherlock Holmes Geschichte präsentiert. So wurde eine längere Interaktion simuliert und wir können messen, wie gut sich das Modell an den Anfang der Unterhaltung erinnert.</p>
                <p>Am Ende des Experiments kannst du sehen, wie gut dein Gedächtnis im Vergleich zu dem der KI abgeschnitten hat.</p>""")
st.html("<p>Drücke auf den Button unten, um mit dem Experiment zu beginnen.</p>")

if st.button("Ich bin bereit", key=f"start_experiment_button"):
    if st.session_state.user_id == "":
        st.session_state.user_id = 'CHANGE_TASK_'+''.join(random.choice('123456789ABCDEFG') for _ in range(5))
        user_repository.create_user(st.session_state.user_id, task="change_detection_task", data={"prolific_id": st.session_state.user_id})
        print(st.session_state.user_id)
        user = user_repository.get_user(st.session_state.user_id)
        if user:
                st.session_state.user = user
    st.switch_page("change_detection_task/pages/presentation_page.py")
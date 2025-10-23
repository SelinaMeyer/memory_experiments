import streamlit as st
from core.scripts import user_repository
import pandas as pd
import time


css = """
.st-key-my_blue_container {
    background-color: rgba(100, 100, 200, 0.3);
}
"""

st.html(f"<style>{css}</style>")

user_repository.set_progress(st.session_state.user_id, 7)
st.write(f"Du hast {st.session_state.correct_answer_count} von {len(st.session_state.shuffled_keys_recognition)} Überschriften richtig eingeordnet.")
dat = {"Du":[st.session_state.correct_answer_count],
       "KI": [6]}
dat_df = pd.DataFrame.from_dict(dat)

time.sleep(2)
st.write("Wie hat die KI im Vergleich abgeschnitten?")
with st.spinner():
    time.sleep(5)
st.bar_chart(dat_df, stack=False, horizontal=True, x_label="Anzahl der richtig eingeordneten Überschriften", y=["Du","KI"], y_label=None)
time.sleep(2)

if st.session_state.correct_answer_count == 6:  
    st.write("Das Sprachmodell hat 6 Überschriften richtig eingeordnet.")
    time.sleep(0.5)
    st.html("<h3>Glückwunsch! Dein Gedächtnis ist genauso gut, wie das unseres Sprachmodells!</h3>")
    time.sleep(0.5)
    st.balloons()
    st.balloons()
elif st.session_state.correct_answer_count > 6:
    st.write("Das Sprachmodell hat 6 Überschriften richtig eingeordnet.")
    time.sleep(0.5)
    st.html("<h3>Wow! Dein Gedächtnis ist sogar besser als das unseres Sprachmodells!</h3>")
    time.sleep(0.5)
    st.balloons()
    st.balloons()
else:
    st.write("Das Sprachmodell hat 6 Überschriften richtig eingeordnet.")
    time.sleep(0.5)
    st.html("<h3>Unser Sprachmodell hat mehr Überschriften richtig eingeordnet als du. Aber keine Sorge, das ist ganz normal!</h3>")

time.sleep(2)   
st.empty()     
with st.container(border=False, key="my_blue_container"):
    st.html("<i><b>Ein paar zusätzliche Details:</b></i>")
    st.html(
        "<p>Als KI haben wir <b>Llama3 8B</b> verwendet. Das ist ein relativ kompaktes Sprachmodell, das sogar auf vielen herkömmlichen Computern lokal laufen kann.</p>"
        "<p>Im Vergleich zu größeren Modellen – wie denen, die hinter ChatGPT stecken – ist es zwar weniger leistungsfähig, dafür aber deutlich ressourcenschonender.</p>"
        "<p>Statt der Bilder, die du gesehen hast, haben wir Llama zwischen der Präsentation der Headlines und dem Gedächtnistest <b>einen 4000 Zeichen langen Abschnitt aus einer Sherlock-Holmes-Geschichte</b> gezeigt.</p>"
    )
    st.html(
        "<p>Die Nachrichtenüberschriften wurden aus dem Englischen übersetzt.</p>"
        "<p>Alle Änderungen an den Headlines wurden von verschiedenen LLMs vorgenommen.</p>"
        "<p>Wir untersuchen, wie sich solche Techniken nutzen lassen, um <b>wahre Nachrichten so anzupassen, dass sie besser im Gedächtnis bleiben</b> – ohne dabei die Kernaussage zu verändern.</p>"
        "<p>Langfristig möchten wir so dazu beitragen, <b>den Einfluss von Fehlinformation und Fake News zu verringern</b>.</p>"
    )
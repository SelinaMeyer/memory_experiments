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

time.sleep(0.5)
st.write("Wie hat die KI im Vergleich abgeschnitten?")
with st.spinner():
    time.sleep(2)
st.bar_chart(dat_df, stack=False, horizontal=False, y_label="Anzahl der richtig eingeordneten Überschriften", x=["Du","KI"], x_label=None)
time.sleep(0.5)

if st.session_state.correct_answer_count == 6:  
    st.write("Das Sprachmodell hat 6 Überschriften richtig eingeordnet.")
    st.html("<h3>Glückwunsch! Dein Gedächtnis ist genauso gut, wie das unseres Sprachmodells!</h3>")
    st.balloons()
    st.balloons()
elif st.session_state.correct_answer_count > 6:
    st.balloons()
    st.balloons()
    st.write("Das Sprachmodell hat 6 Überschriften richtig eingeordnet.")
    st.html("<h3>Wow! Dein Gedächtnis ist sogar besser als das unseres Sprachmodells!</h3>")
else:
    st.write("Das Sprachmodell hat 6 Überschriften richtig eingeordnet.")
    st.html("<h3>Unser Sprachmodell hat mehr Überschriften richtig eingeordnet als du. Aber keine Sorge, das ist ganz normal!</h3>")

        
with st.container(border=False, key="my_blue_container"):
    st.html("<i>Ein paar zusätzliche Details:<i>")
    st.html("<p>Als KI haben wir Llama3 8b verwendet. Dabei handelt es sich um ein relativ kleines LLM, das man auch lokal auf gängigen Computern laufen lassen kann.</p>"
        "<p>Anstatt der Bilder, die du gesehen hast, haben wir Llama zwischen der Präsentation der Headlines und dem Gedächtnistest 4000 Zeichen einer Sherlock Holmes geschichte übergeben.</p>")
    st.html(
        "<p>Die Nachrichtenüberschriften wurden aus dem Englischen übersetzt.</p><p>Alle Änderungen an Headlines wurden durch verschiedene LLMs durchgeführt.</p>" \
        "<p>Wir forschen daran, wie wir diese Techniken nutzen können um wahre Nachrichten so zu ändern, das sie besser in Erinnerung bleiben, ohen dabei die Kernaussage zu verändern.</p>" \
        "<p>Damit möchten wir den Einfluss von Misinformation und Fake News reduzieren.</p>")

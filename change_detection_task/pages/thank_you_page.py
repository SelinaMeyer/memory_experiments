import streamlit as st
from core.scripts import user_repository
import pandas as pd
import time

user_repository.set_progress(st.session_state.user_id, 7)
st.write(f"Du hast {st.session_state.correct_answer_count} von {len(st.session_state.shuffled_keys_recognition)} Überschriften richtig eingeordnet.")
dat = {"Du":[st.session_state.correct_answer_count],
       "KI": [6]}
dat_df = pd.DataFrame.from_dict(dat)

if st.session_state.get("ending_timer") not in st.session_state:
        st.session_state.ending_timer = time.time()
st.fragment(run_every=1)
def auswertung():
    if time.time() - st.session_state.get("ending_timer") < 5:
        st.write("Wie hat die KI im Vergleich abgeschnitten?")
    if time.time() - st.session_state.get("ending_timer") >= 5 and time.time() - st.session_state.get("ending_timer") < 10:
        st.bar_chart(dat_df)
    else: 
        if st.session_state.correct_answer_count == 6:  
            st.write("Glückwunsch! Dein Gedächtnis ist genauso gut, wie das unseres Sprachmodells!")
        elif st.session_state.correct_answer_count > 6:
            st.balloons()
            st.write("Wow! Dein Gedächtnis ist sogar besser als das unseres Sprachmodells!")
            st.write("Das Sprachmodell hat nur 6 Überschriften richtig eingeordnet.")
        else:
            st.write("Unser Sprachmodell hat mehr Überschriften richtig eingeordnet als du. Aber keine Sorge, das ist ganz normal!")
            st.write("Das Sprachmodell hat 6 Überschriften richtig eingeordnet.")
        st.html("<p><span color=blue>Als KI haben wir Llama3 8b verwendet.<br/> Dabei handelt es sich um ein relativ kleines LLM, das man auch lokal auf gängigen Computern laufen lassen kann.<br/>"
        "Anstatt der Bilder, die du gesehen hast, haben wir Llama zwischen der Präsentation der Headlines und dem Gedächtnistest 4000 Zeichen einer Sherlock Holmes geschichte übergeben.</span></p>")

auswertung()
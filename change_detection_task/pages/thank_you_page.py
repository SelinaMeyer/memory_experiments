import streamlit as st
from core.scripts import user_repository

user_repository.set_progress(st.session_state.user_id, 7)
st.write(f"Du hast dir {st.session_state.correct_answer_count} von {len(st.session_state.shuffled_keys_recognition)} Überschriften richtig eingeordnet.")
if st.session_state.correct_answer_count == 28:
    st.write("Glückwunsch! Dein Gedächtnis ist genauso gut, wie das unseres Sprachmodells!")
elif st.session_state.correct_answer_count > 28:
    st.write("Wow! Dein Gedächtnis ist sogar besser als das unseres Sprachmodells!")
    st.write("Das Sprachmodell hat nur 28 Überschriften richtig eingeordnet.")
else:
    st.write("Unser Sprachmodell hat mehr Überschriften richtig eingeordnet als du. Aber keine Sorge, das ist ganz normal!")
    st.write("Das Sprachmodell hat 28 Überschriften richtig eingeordnet.")
st.write("Vielen Dank, dass du an unserem Experiment teilgenommen hast!")
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

st.html("""<p>Im Folgenden siehst du 7 englischsprachige Nachrichtenüberschriften für jeweils 10 Sekunden.</p>
        <p>Präge dir diese Überschriften so gut wie möglich ein. </p>
        <p>Im Anschluss kannst du deine Gedächtnisleistung mit der eines großen Sprachmodells (LLM) messen.</p>
        <p>Drücke auf den Button unten, um mit dem Experiment zu beginnen.""")

if st.button("Ich bin bereit", key=f"start_experiment_button"):
    if st.session_state.user_id == "":
        st.session_state.user_id = 'CHANGE_TASK_'+''.join(random.choice('123456789ABCDEFG') for _ in range(5))
        user_repository.create_user(st.session_state.user_id, task="change_detection_task", data={"prolific_id": st.session_state.user_id})
        print(st.session_state.user_id)
        user = user_repository.get_user(st.session_state.user_id)
        if user:
                st.session_state.user = user
    st.switch_page("change_detection_task/pages/presentation_page.py")
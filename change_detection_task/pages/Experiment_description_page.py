import streamlit as st

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

st.html("""<p>Im Folgenden siehst du 16 englischsprachige Nachrichtenüberschriften für jeweils 10 Sekunden.</p>
        <p>Präge dir diese Überschriften so gut wie möglich ein. Im Anschluss kannst du deine Gedächtnisleistung mit der eines großen Sprachmodells (LLM) messen.</p>
        <p>Drücke auf den Button unten, um mit dem Experiment zu beginnen.""")

if st.button("Ich bin bereit", key="start_experiment_button"):
    st.switch_page("change_detection_task/pages/distractor_page.py")
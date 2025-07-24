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

st.html("""<p>In the following, you will see some news headlines. The headlines will be presented back-to-back, one after the other. Each headline will be presented for 10 seconds. Please read each headline carefully and try to memorize the headline as best as you can.  
        <p><b>Important</b>: Please do not use any external tools to record or write down the headlines. We are interested in how memorable the headlines are for you, relying on nothing but your own memory. 
        <br>Please note that your reward is in no way dependent on how many headlines you may or may not be able to memorize. Thank you for your cooperation!
        <p><b>Please do not use any browser navigation buttons (like "back" or "refresh") during the study.<br>
        To ensure you can finish the study smoothly, make sure you have a stable internet connection and won’t be interrupted or distracted for the next 20 minutes.</b>
        <p>Are you ready to start the study? <br>The first headline will be presented once you click the "Start Experiment" button below.""")

if st.button("Start Experiment", key="start_experiment_button"):
    st.switch_page("memory_experiment_3/pages/presentation_page.py")
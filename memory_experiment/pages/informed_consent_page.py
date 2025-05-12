import streamlit as st
from core.scripts import user_repository, database_repository
from captcha.image import ImageCaptcha
import random, string

length_captcha = 4
width = 200
height = 150
target_id = st.session_state.user_id
user = user_repository.get_user(target_id)
task = st.session_state.task

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

if not user:
        with st.container():
            st.html("<h1>Welcome to this Experiment!")
            st.html("""
<h1>Informed Consent of Participation 
<p>You are invited to participate in the online study "Memorability And Credibility Of News Headlines" initiated and conducted by Dr. Selina Meyer. The research is supervised by Prof. Dr. Michael Roth and Prof. Dr. Magdalena Abel at the UTN Nuremberg. 
                    <br>If you have any questions or complaints about the informed consent process of this research study or your rights as a human research subject, please contact Dr. Selina Meyer (E-Mail: selina.meyer@utn.de). 
                    <br>Please carefully read the information below.
<h2>1. Purpose and Goal of this Research
<p>The purpose of the research project is to identify the dynamics at play in the proliferation of information online. 
                    The goal of this study is to explore to which extent certain linguistic features affect memorability and truthfulness judgements of news headlines. 
                    <br>Your participation will help us achieve this goal. The results of this research and collected data may be presented at scientific or professional meetings or published in scientific proceedings and journals. 
<h2>2. Participation and Compensation
<p>Your participation in this online study is completely voluntary. You will be one of approximately 120 people being surveyed for this research. You will receive 4 GBP as compensation for your participation. 
                    <br>You may withdraw and discontinue participation at any time without penalty or losing the compensation. 
<h2>3. Procedure
<p>In this study, your initial task will be to read and memorize news headlines. 
                    You will then be asked to remember the headlines and to subjectively judge and rate the headlines. 
                    Finally, you will be asked to provide some basic demographic information about yourself. 
                    It should take about 20 minutes to complete the full study.
<h2>4. Risks and Benefits
<p>There are no risks associated with this online study. Discomforts or inconveniences will be minor and are not likely to happen. 
<h2>5. Data Protection and Confidentiality
<p>Some personal data (gender, political affiliation, etc.) will be recorded during participation. You may refuse to answer any questions about yourself you do not want to answer. 
                    No personally identifiable information such as your name, address, or email address will be recorded.
                    All data you provide in this online study will be published anonymized and treated confidentially in compliance with the General Data Protection Regulation (GDPR) of the European Union (EU). 
                    Subsequent uses of records and data will be subject to standard data use policies which protect the full anonymity of the participating individuals. 
                    Despite careful control of content, the researchers assume no liability for damages, which directly or indirectly result from the use of this online application. 
                    As with any publication or online related activity, the risk of a breach of confidentiality is always possible. 
                    According to the GDPR, the researchers will inform the participant if a breach of confidential data was detected. 
<h2>6. Identification of Investigators
<p>If you have any questions or concerns about the research, please feel free to contact: <br>
                    Dr. Selina Meyer <br>
                    selina.meyer@utn.de <br>
                    Natural Language Understanding Lab <br>
                    Department of Computer Science and Artificial Intelligence <br>
                    University of Technology Nuremberg <br>
                    Germany <br>
<p>By clicking the button below and entering your prolific ID, you agree to participate in this experiment and give your consent to the use of your data for research purposes. 
""")
    
            prolific_id = st.text_input("Prolific ID:", max_chars=200)
            agree = st.radio(label="Do you agree to the above information?",label_visibility="hidden",options=["I have read and understood the information above and agree to participate in this experiment", "I do not agree to participate in this experiment"], index=None, key="informed_consent")
        if agree == "I do not agree to participate in this experiment":
            st.warning("If you do not want to participate, please close the window and return the experiment on Prolific.")
        if prolific_id and agree=="I have read and understood the information above and agree to participate in this experiment":
            if "captcha_control" not in st.session_state:
                print("adding captcha control to session state")
                st.session_state.captcha_control = False
            col1, col2 = st.columns(2)
            if "captcha" not in st.session_state:
                print("adding captcha to session state")
                st.session_state.captcha = "".join(random.choices(string.ascii_letters + string.digits, k=length_captcha))
                print("the captcha is: ", st.session_state.captcha)
            Image = ImageCaptcha(width=width, height=height)
            data = Image.generate(st.session_state.captcha)
            col1.image(data)
            captcha_text = col2.text_input("Please enter the captcha text:", max_chars=length_captcha)
            if captcha_text:
                print("Captcha text entered: ", captcha_text)
                if captcha_text == st.session_state.captcha:
                    st.session_state.captcha_control = True
                    st.success("Captcha is correct!")
                    user_repository.create_user(target_id, task=task, data={"prolific_id": prolific_id})
                    user = user_repository.get_user(target_id)
                    st.session_state.user = list(user)
                    st.switch_page("memory_experiment/pages/Experiment_description_page.py")
                else:
                    st.error("Captcha is incorrect. Please try again.")
            if st.button("Generate new Captcha"):
                st.session_state.captcha = "".join(random.choices(string.ascii_letters + string.digits, k=length_captcha))
                print("the captcha is: ", st.session_state.captcha)
                st.rerun()
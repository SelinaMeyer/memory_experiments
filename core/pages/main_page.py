
import streamlit as st

st.session_state.page = "main_page"

if not st.session_state.user_id:
    st.markdown("""
    # Welcome!
                
    This is the annotation website for the Natural Language Understanding Research Group at the University of Technology Nuremberg.

    ## Are you here for annotation?
                
    If you were redirected here for the purpose of annotation, find the 'Log In' option in the sidebar to your left.
    Then, enter the unique annotator ID that we shared with you.
    Once you have successfully logged in, new options will become available to you so you can start reading the introduction and taking the qualification test.
    """)

else:
    st.markdown("""
    # Welcome!
                
    This is the annotation website for the Natural Language Understanding Research Group at the University of Technology Nuremberg.

    ## Are you here for annotation?
                
    **Thanks for taking part in the second round of our annotation task!**  
    Since you already passed the qualification test in the first round, you can proceed directly to the annotation.
    There are only nine samples for you to annotate this time, so it shouldn't take up much of your time.      
    In case you need a refresher on the task, you can find it in the "Headline Rewriting Judgement Intro" Tab
    """)

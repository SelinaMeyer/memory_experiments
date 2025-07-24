import streamlit as st
from core.scripts import user_repository

user_repository.set_progress(st.session_state.user_id, 7)
st.write("Thank you for your participation! We appreciate you taking the time to complete the study.")
st.write("Your responses have been recorded. If you have any questions or concerns, please feel free to reach out to us at selina.meyer@utn.de.")
st.write("To redeem your reward click the link below or copy the Prolific Code: C11C39NE")
st.write("https://app.prolific.com/submissions/complete?cc=C11C39NE")
st.write("You can close this window now.")
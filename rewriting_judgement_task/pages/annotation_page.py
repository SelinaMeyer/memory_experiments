import os

import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, TASK_INFO
from rewriting_judgement_task.common import utils


samples = read_json_from_file(TASK_INFO["rewriting_judgement_task"]["annotation_filepath"])

# Turns out if you dont check that, annotators may start with the wrong sample in the post-qualification grouping option.
if user_repository.get_qualification() == 1:
    if not st.session_state.progress:  # no checkpoint yet -> simply go to the first relevant sample
        st.session_state.progress, keys = utils.skip_to_next_sample(0, samples, st.session_state.user[3], 1, 
                                                        "annotation", qualification_function=None)
    st.session_state.page = "rewrite_judgement_task_annotation_page_sample" + str(st.session_state.progress)

if user_repository.get_qualification() != 1:
    st.write("## You must pass qualification before starting annotation. \n\n Select **Qualification** in the navigation bar to your left to try the qualification test.")
elif user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
else:
    index = int(st.session_state.progress)

    back_button = st.button(label="Back", key = 10 * index + 7, help="Go back to the previous sample.")

    question, accuracy, accuracy_subclass, style, style_subclass, emotion_shift, comment_input, next_input =  utils.print_annotation_schema_sliders("annotation", st.session_state.shuffled_keys[index])

    annotation = {"question": question, "accuracy": accuracy, "accuracy_subclass": accuracy_subclass,
                   "style": style, "style_subclass": style_subclass, "emotion_shift": emotion_shift, "comment": comment_input, "keys": st.session_state.shuffled_keys, "index": index}
    if next_input:
        utils.handle_next_button(annotation, index, samples, "annotation")

    if back_button:
        utils.handle_back_button(annotation, index, samples, "annotation")
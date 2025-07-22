import os

import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, TASK_INFO, finish_subtask
from headline_rewriting_task.common import utils


samples = read_json_from_file(TASK_INFO["headline_rewriting_task"]["annotation_filepath"])

# Turns out if you dont check that, annotators may start with the wrong sample in the post-qualification grouping option.
if user_repository.get_qualification() == 1:
    if "progress" not in st.session_state:  # no checkpoint yet -> simply go to the first relevant sample
        st.session_state.progress, keys = utils.skip_to_next_sample(0, samples, st.session_state.user[3], 0, 
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

    question, revision, not_revisable, comment_input, next_input =  utils.print_revision_schema("annotation", int(st.session_state.shuffled_keys[index]))
    progression_data = {}
    progression_data["keys"] = st.session_state.shuffled_keys
    progression_data["index"] = index
    print("Progression data", progression_data)
    annotation = {"sample_id": st.session_state.shuffled_keys[index], "question": question, "revision": revision, 
                  "revision_not_possible": not_revisable, "comment": comment_input}
    
    rewritten_count = user_repository.get_rewritten_count(st.session_state.user_id)
    print(rewritten_count)

    if next_input:
        print("Next input received")
        if index >= len(st.session_state.shuffled_keys) - 1:
            print("finishing subtask")
            user_repository.save_one_annotation(st.session_state.user_id, "annotation", int(st.session_state.shuffled_keys[index]), annotation)
            finish_subtask()
        elif rewritten_count >= 14:
            print("finishing subtask")
            user_repository.save_one_annotation(st.session_state.user_id, "annotation", int(st.session_state.shuffled_keys[index]), annotation)
            finish_subtask()
        else: 
            print(len(st.session_state.shuffled_keys))
            print("index smaller than shuffled key length and number revisions is less than 15")
            print("Current index: ", index)
            print("Current sample:", st.session_state.shuffled_keys[index])
            user_repository.update_demographics(st.session_state.user_id, progression_data)
            utils.handle_next_button(annotation, index, samples, "annotation")

    if back_button:
        user_repository.update_demographics(st.session_state.user_id, progression_data)
        utils.handle_back_button(annotation, index, samples, "annotation")
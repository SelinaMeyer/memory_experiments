import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO, finish_subtask
from core.scripts import user_repository, database_repository

import random

def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"

def print_annotation_schema_sliders(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema for the annotation with the sliders. 

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["rewriting_judgement_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["rewriting_judgement_task"]["annotation_filepath"])

    '''sample_preload = load_annotation(subtask, index)
    if not sample_preload:
        value_slider, value_nonsensical, value_comment = None, None, ""
    else:
        value_slider, value_nonsensical, value_comment = (sample_preload["slider"], sample_preload["nonsensical"], sample_preload["comment"])
        if value_slider in slider_labels:
            value_slider = slider_labels[value_slider]
        else:
            value_slider = None'''

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("Read the following headline and revision")

    st.write("---")

    st.markdown("**Original**: " + question["original"])

    st.write("---")

    st.markdown("**Revision**: " + question["revision"])

    st.write("---")

    accuracy = st.radio("Does the content in the revised version accurately reflect the content of the source text?",
                        ["Yes", "No"], key=5+index, index=None)
    
    misrepresentation, omission, addition = False, False, False
    if accuracy == "No":
        accuracy_col = st.columns(3)
        with accuracy_col[0]:
            misrepresentation = st.checkbox("Misrepresentation")
        with accuracy_col[1]:
            omission = st.checkbox("Omission")
        with accuracy_col[2]:
            addition = st.checkbox("Addition")

    if st.toggle("Show guidelines for rating accuracy"):
        st.markdown("""
**Select "no" if any of the following violations are found in the revision and check all that apply:**

* **Misrepresentation**: the revision misrepresents information provided in the original headline
* **Addition**: The revision includes content not present in the original headline
* **Omission**: The revision is missing content present in the original headline
        """)
    accuracy_subclass = [misrepresentation, omission, addition]

    st.write("\n")

    style = st.radio("Is the language style of the revised headline appropriate?",
                        ["Yes", "No"], key=10+index, index=None)
    
    grammar, awkward, inconsistent = False, False, False
    if style == "No":
        style_col = st.columns(3)
        with style_col[0]:
            grammar = st.checkbox("Grammar")
        with style_col[1]:
            awkward = st.checkbox("Awkward Style")
        with style_col[2]:
            inconsistent = st.checkbox("Inconsistent Style")

    style_subclass = [grammar, awkward, inconsistent]

    if st.toggle("Show guidelines for rating style"):
        st.markdown("""          
**Check "no" if any of the following are found in the revision and check all that apply:**
* **Grammar**: The revision contains grammar or language errors
* **Awkward Style**: The revision is grammatical, but unnatural as a news headline or awkward (e.g it involves excessive wordiness or overly embedded clauses)
* **Inconsistent Style**: The style or tone is inconsistent within the revision (e.g. factual, dry information is paired with sensationalism)
        """)
    st.write("\n\n")

    emotion_shift = st.checkbox("The revision differs in tone or emotion compared to the original", key = 5*index+3)

    comment_input = st.text_input(key = 10 * index + 8, label = "Comments (optional)", value="", help="Optional free text for comments and thoughts", max_chars=1000)

    if accuracy and style:
        next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None

    return_sample = {
        "index": str(index),
        "original": question["original"],
        "revision": question["revision"],
    }
    
    return return_sample, accuracy, accuracy_subclass, style, style_subclass, emotion_shift, comment_input, next_input

def get_item_progress(user_id:str):
    conn = st.session_state.conn
    cursor = conn.cursor()

    cursor.execute(f"SELECT data FROM user_data WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    data = result[0]
    stage_index = data.get("index", 0)

    stage_index = data.get("shuffled_keys", )

    return stage_index

def skip_to_next_sample(index: int, samples: dict, grouping: int, direction: int=1, 
                        subtask: str="annotation", qualification_function=None) -> int:
    """
    From the specified index, move in the specified direction to find the next sample relevant to the group.

    :param index: Index of the current page/sample
    :param samples: dict of all the samples (keys are "1", "2", ...)
    :param grouping: group of user
    :param direction: 1 for going forward, -1 for going backward
    :param subtask: e.g. annotation or qualification
    :param qualification function: Function to evaluate whether qualification was passed, not needed if subtask!=qualification
    :return: Index of the next (or previous) sample
    """

    shuffled_keys, index = user_repository.get_item_progress("keys", st.session_state.user_id)

    if shuffled_keys not in st.session_state:
        st.session_state.progress = user_repository.get("annotation")
        if not shuffled_keys:
            print("No shuffled keys found, creating new ones")
            shuffled_keys = [key for key, value in samples.items() if value["grouping"] == st.session_state.user[3]]
            random.shuffle(shuffled_keys)
            index = 0

    st.session_state.shuffled_keys = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys)
    st.session_state.index = index
    print("current index:", st.session_state.index)

    index += direction

    return index


def handle_back_button(annotation: dict, index: int, samples: dict, subtask="annotation"):
    """
    All-in-one behaviour of the back button: Saves revised annotations and skips to the next-oldest relevant sample.

    :param annotation: The annotation of the currently displayed sample
    :param index: The index of the current sample
    :param samples: List with all of the samples (including irrelevant ones for the grouping) for the current subtask
    :param subtask: The current subtask, e.g. annotation or qualification
    """
    # don't save when pressing back on the newest sample, since it will otherwise get skipped when returning later
    if index < user_repository.get_checkpoint(key=subtask, print=False):
        user_repository.save_one_annotation(st.session_state.user_id, subtask, index, annotation)

    grouping = st.session_state.user[3]
    # skip backwards over the samples of the other groups to arrive at the new index
    new_index = skip_to_next_sample(index, samples, grouping, direction=-1)

    if subtask == "qualification":
        st.session_state.qualification_progress = new_index
    else:
        st.session_state.progress = new_index

    st.rerun()



def handle_next_button(annotation: dict, index: int, samples: dict, subtask="annotation", qualification_function=None):
    """
    All-in-one behaviour of the next button: Saves annotation, skips to next relevant sample and finishes the annotation if the end is reached.
    
    :param annotation: The annotation of the current sample that should be saved.
    :param index: The index of the current sample
    :param samples: List with all of the samples (including irrelevant ones for the grouping) for the current subtask
    :param subtask: The current subtask, e.g. annotation or qualification
    :param qualification_function: If subtask=qualification, a function that evaluates success of qualification given user annotations
    """
    user_repository.save_one_annotation(st.session_state.user_id, subtask, index, annotation)

    if index >= len(samples):
        finish_subtask(subtask, qualification_function=qualification_function)
    else:
        grouping = st.session_state.user[3]
        # proceed until we find the next sample relevant for the grouping
        new_index = skip_to_next_sample(index, samples, grouping, direction=1)

    if subtask == "qualification":
        st.session_state.qualification_progress = new_index
    else:
        st.session_state.progress = new_index

    if new_index != index:
        st.rerun()
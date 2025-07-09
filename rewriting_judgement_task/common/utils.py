import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO


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
    
    grammar, awkward, register, inconsistent = False, False, False, False
    if style == "No":
        style_col = st.columns(4)
        with style_col[0]:
            grammar = st.checkbox("Grammar")
        with style_col[1]:
            awkward = st.checkbox("Awkward Style")
        with style_col[2]:
            register = st.checkbox("Register")
        with style_col[3]:
            inconsistent = st.checkbox("Inconsistent Style")

    style_subclass = [grammar, awkward, register, inconsistent]

    if st.toggle("Show guidelines for rating style"):
        st.markdown("""          
**Check "no" if any of the following are found in the revision and check all that apply:**
* **Grammar**: The revision contains grammar or language errors
* **Awkward Style**: The revision is grammatical, but unnatural as a news headline or awkward (e.g it involves excessive wordiness or overly embedded clauses)
* **Register**: The revision does not match the tone or level of formality exhibited by the original headline. The inclusion of first/second person pronouns generally changes how personal the headline is, which in this case does not qualify as a shift in formality
* **Inconsistent Style**: The style or tone is inconsistent within the revision (e.g. factual, dry information is paired with sensationalism)
        """)
    st.write("\n\n")

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
    
    return return_sample, accuracy, accuracy_subclass, style, style_subclass, comment_input, next_input

def get_item_progress(current_stage:str, user_id:str):
    conn = st.session_state.conn
    cursor = conn.cursor()

    cursor.execute(f"SELECT data FROM user_data WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    data = result[0]
    stage_result = data.get(current_stage, [])
    stage_index = data.get("index", 0)

    return stage_result, stage_index

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
    index += direction
    if index < 1:
        return 1
    while True:
        if index > len(samples):
            finish_subtask(subtask, qualification_function)
            break
        if str(index) not in samples:  # account for samples having id gaps
            index += direction
            continue
        checked_sample = samples[str(index)]
        if ("grouping" not in checked_sample) or (grouping == checked_sample["grouping"]):
            break  # break when finding relevant sample
        else:
            index += direction
            if index < 1:  # went back too far
                index = 1
                direction = 1  # reverse to find first sample again
    # return index where it found a sample
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
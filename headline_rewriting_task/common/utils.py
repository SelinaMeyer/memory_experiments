import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO, finish_subtask
from core.scripts import user_repository, database_repository

import random

def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"


def print_revision_schema(subtask:str, index:int) -> tuple:
    """
    Prints the revision schema for the annotation task.

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """

    samples = read_json_from_file(TASK_INFO["headline_rewriting_task"]["annotation_filepath"])

    sample_preload = load_annotation(subtask, index)
    if not sample_preload:
        revision = ""
    else:
        revision = sample_preload["revision"]

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("Read the following headline and revise it to include a first or second person pronoun. Make sure your revision retains the original content and tone.")

    st.write("---")

    st.markdown("**Original**: " + question["original"])

    st.write("---")

    revision = st.text_area(label="Your headline revision", value=revision, key=f"revision_{index}")
    not_revisable = st.checkbox(label="I cannot revise this headline in the specified way", key=f"not_revisable_{index}", value=False)

    st.write("---")

    comment_input = st.text_area(label="Optional comment on your revision", key=5*index+8, value=sample_preload["comment"] if sample_preload else "")

    next_input = None
    if revision != "":
        next_input = st.button(
            label="Next",
            key=f"next_button_{index}",
            help="Save this annotation and advance to the next one."
        )
    elif not_revisable:
        next_input = st.button(
            label="Next",
            key=f"next_button_not_revisable_{index}",
            help="Save this annotation and advance to the next one."
        )

    return question, revision, not_revisable, comment_input, next_input
    
   
def print_annotation_schema_sliders(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema for the annotation with the sliders. 

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    
    samples = read_json_from_file(TASK_INFO["headline_rewriting_task"]["qualification_filepath"])

    sample_preload = load_annotation(subtask, index)
    if not sample_preload:
        value_accuracy, value_style = None, None
    else:
        value_accuracy, value_style = (sample_preload["accuracy"], sample_preload["style"])

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("Read the following headline and revision")

    st.write("---")

    st.markdown("**Original**: " + question["original"])

    st.write("---")

    st.markdown("**Revision**: " + question["revision"])

    st.write("---")

    radio_index_dict = {"Yes": 0, "No": 1, None: None}

    accuracy = st.radio("Does the content in the revised version accurately reflect the content of the source text?",
                        ["Yes", "No"], key=5*index+8, index=radio_index_dict[value_accuracy])

    if st.toggle("Show guidelines for rating accuracy"):
        st.markdown("""
**Select "no" if any of the following violations are found in the revision:**

* **Misrepresentation**: the revision misrepresents information provided in the original headline
* **Addition**: The revision includes content not present in the original headline
* **Omission**: The revision is missing content present in the original headline
        """)

    st.write("\n")

    style = st.radio("Is the language style of the revised headline appropriate?",
                        ["Yes", "No"], key=10*index+9, index=radio_index_dict[value_style])

    if st.toggle("Show guidelines for rating style"):
        st.markdown("""          
**Check "no" if any of the following are found in the revision:**
* **Grammar**: The revision contains grammar or language errors
* **Awkward Style**: The revision is grammatical, but unnatural as a news headline or awkward (e.g it involves excessive wordiness or overly embedded clauses)
* **Inconsistent Style**: The style or tone is inconsistent within the revision (e.g. factual, dry information is paired with sensationalism)
        """)
    st.write("\n\n")

    can_enable_next = False

    if accuracy and style:
        can_enable_next = True

    next_input = None
    if can_enable_next:
        next_input = st.button(
            label="Next",
            key=f"next_button_{index}",
            help="Save this annotation and advance to the next one."
        )

    return_sample = {
        "index": str(index),
        "original": question["original"],
        "revision": question["revision"],
    }
    
    return return_sample, accuracy, style, next_input

def get_item_progress(user_id:str):
    conn = st.session_state.conn
    cursor = conn.cursor()

    cursor.execute(f"SELECT data FROM user_data WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if not result:
        return 0, []
    print(result)
    data = result[0]
    index = data.get("index", 0)
    keys = data.get("keys", [])

    return index, keys

def skip_to_next_sample(index: int, samples: dict, grouping: int, direction: int=1, 
                        subtask: str="annotation", qualification_function=None) -> tuple[int, list]:
    """
    From the specified index, move in the specified direction to find the next sample relevant to the group.

    :param index: Index of the current page/sample
    :param samples: dict of all the samples (keys are "1", "2", ...)
    :param grouping: group of user
    :param direction: 1 for going forward, -1 for going backward
    :param subtask: e.g. annotation or qualification
    :param qualification function: Function to evaluate whether qualification was passed, not needed if subtask!=qualification
    :return: Tuple (index of the next sample, list of shuffled keys)
    """
    if "shuffled_keys" not in st.session_state:
        print("Getting item progress")
        index, shuffled_keys = get_item_progress(st.session_state.user_id)
        if not shuffled_keys:
            print("No shuffled keys found, creating new ones")
            shuffled_keys = [key for key, value in samples.items()]
            random.shuffle(shuffled_keys)
            index = 0

        st.session_state.shuffled_keys = shuffled_keys
        print("Added shuffled keys:", st.session_state.shuffled_keys)
        st.session_state.progress = index
        print("current index:", st.session_state.progress)
    print("Session state keys in skip function", st.session_state.shuffled_keys)
    #index = st.session_state.index
    #shuffled_keys = st.session_state.shuffled_keys
    print("shuffled_keys:", st.session_state.shuffled_keys)
    print("index:", index)
    print("Direction:", direction)
    index += direction

    return index, st.session_state.shuffled_keys


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
        user_repository.save_one_annotation(st.session_state.user_id, subtask, int(st.session_state.shuffled_keys[index]), annotation)

    grouping = st.session_state.user[3]
    # skip backwards over the samples of the other groups to arrive at the new index
    new_index, keys = skip_to_next_sample(index, samples, grouping, direction=-1)

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
    user_repository.save_one_annotation(st.session_state.user_id, subtask, int(st.session_state.shuffled_keys[index]), annotation)

    if st.session_state.progress >= len(st.session_state.shuffled_keys):
        finish_subtask(subtask, qualification_function=qualification_function)
    else:
        print("Index passed to next saple function", index)
        print(st.session_state.shuffled_keys)
        grouping = st.session_state.user[3]
        # proceed until we find the next sample relevant for the grouping
        new_index, keys = skip_to_next_sample(index, samples, grouping, direction=1)

    if subtask == "qualification":
        st.session_state.qualification_progress = new_index
    else:
        st.session_state.progress = new_index

    if new_index != index:
        st.rerun()
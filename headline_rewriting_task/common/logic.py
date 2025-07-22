from core.scripts.utils import read_json_from_file, TASK_INFO

def check_if_qualified(annotations: dict) -> bool:
    """
    Check if the given annotations (from a user's annotation field) would pass the qualification test.

    :param annotations: user's annotation in dict form, should have a 'qualification' key
    :return bool: True if passed, False if not
    """
    qualification_questions = read_json_from_file(TASK_INFO["rewriting_judgement_task"]["qualification_filepath"])

    needed_accuracy_score = 3
    needed_style_score = 3
    accuracy_score = 0
    style_score = 0
    for question_id in qualification_questions:
        if annotations["qualification"][int(question_id)]["accuracy"] == qualification_questions[question_id]["correct_accuracy_answer"]:
            accuracy_score += 1
        if annotations["qualification"][int(question_id)]["style"] == qualification_questions[question_id]["correct_style_answer"]:
            style_score += 1
    
    if (accuracy_score >= needed_accuracy_score and style_score >= needed_style_score):
        return True
    else:
        return False
def process_options(data):
    options = {}
    for page in data["pages"]:
        page_id = page["id"]
        for question in page["questions"]:
            question_id = question["id"]
            if "answers" in question:
                for choice in question["answers"]["choices"]:
                    choice_id = choice["id"]
                    choice_text = choice.get("text", f"Choice {choice_id}")
                    options[question_id, choice_id] = choice_text
            elif question["family"] == "open_ended":
                question_text = question["headings"][0]["heading"]
                options[(question_id, None)] = question_text
    return options
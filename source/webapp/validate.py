def task_validate(name, description, status, date):
    errors = {}
    if not name:
        errors["name"] = "The field is mandatory"
    elif len(name) > 50:
        errors["name"] = "There should be less than 50 characters"
    if not description:
        errors["description"] = "The field is mandatory"
    elif len(description) > 100:
        errors["author"] = "There should be less than 100 characters"
    if not status:
        errors["status"] = "The field is mandatory"
    elif len(status) > 50:
        errors["status"] = "There should be less than 50 characters"
    if not date:
        errors["date"] = "The field is mandatory"
    elif len(status) > 50:
        errors["date"] = "There should be less than 50 characters"
    return errors
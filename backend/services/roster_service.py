"""Checks the columns of an uploaded roster file."""


def validate_roster(dataframe_columns):
    required = {"student_id", "name", "department"}
    cols = set(dataframe_columns)
    errors = []
    missing = required - cols
    if missing:
        errors.append(f"Missing required columns: {', '.join(sorted(missing))}")
    extra = cols - required
    if extra:
        errors.append(f"Unexpected columns: {', '.join(sorted(extra))}")
    return errors

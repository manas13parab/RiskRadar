"""Password helpers. Passwords are stored hashed, never as plain text."""
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)


def default_student_password(first_name, student_id):
    """First login password of a student: firstname@number, e.g. omar@1000."""
    number = student_id[1:]
    return f"{first_name.lower()}@{number}"

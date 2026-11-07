"""Routes: connects every web address to a function. Endpoint names are the ones the templates use."""
from backend.routes import auth_routes, student_routes, teacher_routes


def register_routes(app):
    auth_routes.register(app)
    teacher_routes.register(app)
    student_routes.register(app)

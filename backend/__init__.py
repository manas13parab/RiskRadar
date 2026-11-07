"""
RiskRadar backend package.

Layers (each one only talks to the layer below it):
    routes/        web addresses (Flask) -> call services
    services/      the app's actions (login, predict, stats...) -> call repositories and ml/
    repositories/  SQL queries
    db/            connection, tables, first-run seeding
"""

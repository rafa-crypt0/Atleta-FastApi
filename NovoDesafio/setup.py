from setuptools import setup, find_packages

setup(
    name="workout_api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "pydantic-settings",
        "SQLAlchemy",
        "alembic",
        "asyncpg",
        "python-dotenv",
        "fastapi-pagination",
    ],
)

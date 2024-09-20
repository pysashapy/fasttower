from setuptools import setup, find_packages

setup(
    name="fasttower",
    version="0.1.0",
    description="A Django-like framework built on FastAPI",
    long_description_content_type="text/markdown",
    author="Alexander Ibragmov",
    author_email="sasha.2000ibr@gmail.com",
    url="https://github.com/pysashapy/FastTower",
    packages=find_packages(exclude=["tests", "example"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "typer==0.12.5",
        "fastapi==0.115.0",
        "tortoise-orm==0.21.6",
        "aerich==0.7.2",
        "scrypt==0.8.24",
        "Jinja2==3.1.4",
        "uvicorn==0.30.6",
    ],
    entry_points={
        "console_scripts": [
            "tower=fasttower.cli:app",
        ],
    },
)

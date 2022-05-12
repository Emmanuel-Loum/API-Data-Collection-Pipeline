import setuptools
from setuptools import setup
from setuptools import find_packages



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Emmanuel-Loum",
    version="0.0.1",
    author="Emmanuel",
    author_email="oryemaprince62@gmail.com",
    description="Data Collection package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Emmanuel-Loum/Computer-Vision-Rock-Paper-Scissors",
    project_urls={
        "Bug Tracker": "https://github.com/Emmanuel-Loum/Computer-Vision-Rock-Paper-Scissors/Documentation",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CC0 1.0 Universal",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)

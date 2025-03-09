from setuptools import setup, find_packages

setup(
    name="rasa_customizable_framework",
    version="0.1.0",  # Updated to semantic versioning
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open("requirements.txt").readlines()
    ],
    entry_points={
        "console_scripts": [
            "run-actions=rasa_sdk.__main__:main",
        ],
    },
    include_package_data=True,
    description="A customizable Rasa chatbot framework for business automation",
    author="Mateus Anjos",
    author_email="anjosmat14@gmail.com",  # Please update this
    url="https://github.com/Anjosmat/Rasa_Customizable_Framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Rasa",  # Added relevant classifier
        "Intended Audience :: Developers",  # Added relevant classifier
    ],
    python_requires=">=3.10",
)

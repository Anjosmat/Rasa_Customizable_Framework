from setuptools import setup, find_packages

setup(
    name="rasa_customizable_framework",
    version="0.1",
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
    author_email="your-email@example.com",
    url="https://github.com/Anjosmat/Rasa_Customizable_Framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

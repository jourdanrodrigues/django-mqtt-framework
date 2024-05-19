from setuptools import find_packages, setup

with open("requirements-dev.txt") as requirements_file:
    dev_dependencies = requirements_file.read().strip().split("\n")

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="python-mqtt-framework",
    version="0.0.5",
    description="An opinionated framework to handle MQTT communication in Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Jourdan Rodrigues",
    author_email="thiagojourdan@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/jourdanrodrigues/python-mqtt-framework",
    python_requires=">=3.8",
    packages=find_packages(include=["mqtt_framework"]),
    install_requires=[
        "paho-mqtt>=2.0",
    ],
    extras_require={"dev": [dev_dependencies]},
)

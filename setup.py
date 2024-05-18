from setuptools import find_packages, setup

with open("requirements-dev.txt") as f:
    dev_dependencies = f.read().strip().split("\n")

setup(
    name="django-mqtt-framework",
    version="0.0.1",
    description="",
    author="Jourdan Rodrigues",
    author_email="thiagojourdan@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
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
    url="https://github.com/jourdanrodrigues/django-mqtt-framework",
    python_requires=">=3.12",
    packages=find_packages(include=["mqtt_framework"]),
    install_requires=[
        "django>=3.2",
        "paho-mqtt>=2.0",
    ],
    extras_require={"dev": [dev_dependencies]},
)

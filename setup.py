import os
from setuptools import setup, find_packages

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))
README_FILE = open(os.path.join(PACKAGE_ROOT, "README.md"), "r").read()

if __name__ == "__main__":
    setup(
        name="powergrader-event-utils",
        version="0.3.0",
        description="Apporto PowerGrader Utils",
        long_description=README_FILE,
        long_description_content_type="text/markdown",
        author="WhaleCoded",
        author_email="d.hutchison@apporto.com",
        python_requires=">=3.12",
        packages=find_packages(),
        install_requires=["kafka-python", "protobuf", "strenum", "confluent-kafka"],
        extras_require={"dev": ["pytest", "black"]},
    )

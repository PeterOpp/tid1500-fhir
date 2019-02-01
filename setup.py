import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "dsr2fhir",
    version = "0.0.1",
    author = "Hans Meine, Peter Oppermann",
    author_email = "hans.meine@mevis.fraunhofer.de, peter.oppermann@mevis.fraunhofer.de",
    description = "Converting a DICOM SR file (TID 1500) into FHIR resources",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/hmeine/tid1500-fhir",
    packages = setuptools.find_packages(),
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    ],
    entry_points = {
        'console_scripts': ['dsr2fhir=dsr2fhir.main:main'],
    },
    setup_requires = ["pytest-runner"],
    tests_require = ["pytest", "json_compare", "requests"],
)

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="justogres",
    version="2.0.6",
    author=["Jose Izam", "Daniel Taiba"],
    author_email=["jose.izam99@gmail.com", "danielt.dtr@gmail.com"],
    description="Pass postgres data to pandas dataframe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justo-bi/justogres",
    project_urls={
        "Bug Tracker": "https://github.com/justo-bi/justogres",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires = [
        'numpy==1.22.3',
        'pandas==1.2.2',
        'psycopg2-binary==2.9.3',]
)
from setuptools import setup

setup(
    name="PyForks",
    version="0.0.18",
    author="Trailforks Python Library",
    author_email="josh@mn-mtb.com",
    packages=["PyForks", "PyForks._test"],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/cribdragg3r/PyForks/issues",
        "Funding": "https://donate.pypi.org",
        "Source": "https://github.com/cribdragg3r/PyForks",
        "Documentation": "https://pyforks.mn-mtb.com",
    },
    url="http://pypi.python.org/pypi/PyForks/",
    license="LICENSE.txt",
    description="A package to interface with Trailforks.com",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    package_data={
        'PyForks': ['PyForks/data/region_data.parquet']
        },
    install_requires=[
        "pytest",
        "tqdm",
        "requests",
        "pandas",
        "pyarrow"
    ],
)

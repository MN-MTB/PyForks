from setuptools import setup

setup(
    name="PyForks",
    version="1.0.0",
    author="Joshua Faust",
    author_email="josh@mn-mtb.com",
    packages=["PyForks"],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/MN-MTB/PyForks/issues",
        "Funding": "https://account.venmo.com/u/mnmtb",
        "Source": "https://github.com/MN-MTB/PyForks/PyForks",
        "Documentation": "https://pyforks.mn-mtb.com",
    },
    url="http://pypi.python.org/pypi/PyForks/",
    license="LICENSE.txt",
    description="Python library for the Trailforks API",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    include_package_data=True,
    package_data={
        '': ['data/region_data.parquet']
        },
    install_requires=[
        "requests"
    ],
)

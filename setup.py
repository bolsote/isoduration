from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="isoduration",
    version="20.11.0",
    author="Víctor Muñoz",
    author_email="victorm@marshland.es",
    description="Operations with ISO 8601 durations",
    url="https://github.com/bolsote/isoduration",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["arrow>=0.15.0"],
    python_requires=">=3.7",
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Repository": "https://github.com/bolsote/isoduration",
        "Bug Reports": "https://github.com/bolsote/isoduration/issues",
        "Changelog": "https://github.com/bolsote/isoduration/blob/master/CHANGELOG",
    },
    keywords=[
        "datetime",
        "date",
        "time",
        "duration",
        "duration-parsing",
        "duration-string",
        "iso8601",
        "iso8601-duration",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

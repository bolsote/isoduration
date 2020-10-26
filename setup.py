from setuptools import setup, find_packages


setup(
    name="isoduration",
    version="20.10.0",
    author="Víctor Muñoz",
    author_email="victorm@marshland.es",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["arrow>=0.15.0"],
    python_requires=">=3.7",
    zip_safe=False,
)

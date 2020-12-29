import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hex_maze",
    version="0.0.1",
    author="Balthasar Hofer",
    author_email="lebalz@outlook.com",
    description="Create random hexagonal mazes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lebalz/hex-maze",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="perp-py",
    version="0.0.1",
    author="Udit Gulati",
    author_email="uditgulati0@gmail.com",
    description="Python SDk for Perpetual Protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udit-gulati/perp-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'web3 >= 15.20.0',
    ],
)

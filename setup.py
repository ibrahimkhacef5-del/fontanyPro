from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fontany",
    version="1.0.0",
    author="ibrahimkhacef5-del",
    description="Convert any font to MT Manager (MTZ) format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ibrahimkhacef5-del/fontany",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "fonttools>=4.0.0",
        "brotli>=1.0.9",
    ],
    entry_points={
        "console_scripts": [
            "fontany=fontany.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)

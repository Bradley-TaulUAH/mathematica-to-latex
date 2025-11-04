#!/usr/bin/env python3
"""
Setup script for mathematica-to-latex converter
"""

from setuptools import setup
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="mathematica-to-latex",
    version="1.0.0",
    description="Convert Wolfram Mathematica notebook files (.nb) to LaTeX format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bradley Taul",
    author_email="bat0025@uah.edu",
    url="https://github.com/Bradley-TaulUAH/mathematica-to-latex",
    py_modules=["mathematica_to_latex"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Scientific/Engineering",
    ],
    keywords="mathematica latex conversion notebook academic",
    entry_points={
        "console_scripts": [
            "mathematica-to-latex=mathematica_to_latex:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/Bradley-TaulUAH/mathematica-to-latex/issues",
        "Source": "https://github.com/Bradley-TaulUAH/mathematica-to-latex",
    },
)

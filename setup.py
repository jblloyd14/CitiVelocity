from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="citivelocity",
    version="0.1.01",
    author="Your Name",
    author_email="blloyd@finblocks.com",
    description="A Python client for interacting with CitiVelocity API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/citivelocity",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        # Add your project's dependencies here
        # e.g., 'requests>=2.25.0',
        'requests>=2.25.0', 'pandas>=1.1.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

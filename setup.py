from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define requirements directly
requirements = ["pydantic>=1.10.0,<2.0.0", "typing-extensions>=4.0.0"]

setup(
    name="pd-ai-agent-core",
    version="0.0.2",
    author="Parallels",
    author_email="carlos.lapao@parallels.com",
    description="A core library for AI agent functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Parallels/pd-ai-agent-core",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)

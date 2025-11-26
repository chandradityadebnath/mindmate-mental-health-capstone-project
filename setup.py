from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read dependencies from requirements.txt
def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        return [line.strip() for line in content.split("\n") if line.strip()]

setup(
    name="mental-health-agent",
    version="0.1.0",
    author="Team Dynamo",
    description="A creative, smart, and extensible system designed to offer personalized mental-health assistance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chandradityadebnath/mental-health-agent-capstone-project",
    
    # 🌟 KEY CHANGE 1: Find packages inside the 'src' directory
    packages=find_packages(where="src"),
    
    # 🌟 KEY CHANGE 2: Define the package root as 'src'
    package_dir={"": "src"},

    install_requires=read_requirements(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    
    # Entry point if you want to run the agent directly via command line (optional)
    entry_points={
        'console_scripts': [
            'mha-run=mental_health_bot.main:main', # Example entry point
        ],
    },
)

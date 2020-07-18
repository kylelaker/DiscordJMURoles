from setuptools import setup
import re

version = ''
with open('lazybot/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name="lazybot",
    url="https://github.com/ajsnarr98/DiscordJMURoles",
    version=version,
    packages=['lazybot'],
    license="GPLv3",
    description="A Discord bot for helping change roles in JMU Grad Discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "GitPython>=3.1.7,<4.0",
        "discord.py>=1.3.4,<1.4",
    ],
    python_requires=">=3.7",
)
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gurux_net",
    version="1.0.1",
    author="Gurux Ltd",
    author_email="gurux@gurux.org",
    description="Gurux network media is used to commmunication with TCP/IP or UDP connections.",
    long_description="Gurux network media is used to commmunication with TCP/IP or UDP connections.",
    long_description_content_type="text/markdown",
    url="https://github.com/gurux/gurux.net.python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)

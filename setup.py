import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requirements = ['selenium==3.141.0']

setuptools.setup(
    name="srapper",
    version="0.0.1",
    author="Patricio Moracho",
    author_email="pmoracho@gmail.com",
    description="Scrapper de ciertas páginas útiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pmoracho/scrapper",
    packages=setuptools.find_packages(),
    package_data={
        'scrapper': ['scrapper.cfg'],
    },
    entry_points={
        'console_scripts': [
            'scrapper=scrapper.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
    install_requires=install_requirements,
)

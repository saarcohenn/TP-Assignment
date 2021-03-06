# Trusted Partners Assignment

## Background

### Goal

Create a command-line application that, given a list of website URLs as input, visits them and finds, extracts and outputs the websites’ logo image URLs and all phone numbers (e.g. mobile phones, land lines, fax numbers) present on the websites.

### Requirements

• ​Write the application in Python (3.5 or above).
• ​Structure the Python project according to best practices.
• ​Commit all code into a git repository.
• ​Feel free to combine and use any other technology, library and external resource.
• ​The application visits a given input website and outputs the website’s logo, and any found phone numbers. The application should receive a list of website URLs via standard input, one per line. It should write its results to standard output, one per line, unordered, in JSON format. Any logs should be output to standard error. Find examples of the input and output formats in the Examples section below.
• ​The application should process the inputs concurrently. Running it given 50
websites should output most results significantly faster than running it 50 times
given 1 website.
• ​Create a Dockerfile that builds an image containing the ready-to-run command-line application. One should be able to invoke “docker run” and give it input via stdin
instead of having to manually install and run a Python package.
• ​Light cleaning of the found phone numbers should be performed: replace any characters that are not digits, a plus sign (+) or parentheses with whitespace, e.g. clean “+(385)/98 718-2222” into “+(385) 98 718 222”.
• ​If a logo image URL is found, it should be output as an absolute URL, e.g. "http://www.website.com/path/to/logo.png”, not “/path/to/logo.png”.
• ​Don’t worry about handling Flash websites, websites generated dynamically
through Javascript, phone numbers represented as images on the website or any other similar scenario that significantly ramps up the project’s complexity.

### Sources

The following are useful sources of instructions:

1. Selenium [Documentation](https://www.selenium.dev/documentation/)
2. Creating regular Expressions using [Regex101.com](https://regex101.com/)

## Instructions

The following git repository is a solution for Trusted Partners' assignment.

### Installation

1. Clone the repository into a local directory
2. Create a virtual environment using
   - Linux and MacOS: `python3 -m venv virtual_environment_name`
   - Windows: `py -m venv venv virtual_environment_name`
3. Activate the virtual environment:
   - Linux and MacOS: `source virtual_environment_name/bin/activate`
   - Windows: `.\virtual_environment_name\Scripts\activate`
4. To Deactivate the virtual environment, Run `deactivate`
5. Run `pip install -r requirements.txt` to install all dependencies

### Create a docker image

Run The following command to create a docker image:
`docker build . -t tpimage -f ./Dockerfile`

### Run application

You can run the application using a few ways:

1. Run it with the local `website.txt` file [DEBUG MODE]
   - Uncomment the DEBUG section and comment the STREAM section or vice versa.
   - Run `python Scraper.py`
2. To stream a file, run:
   - `python Scraper.py websites.txt` or `cat websites.txt | python Scraper.py`
3. Use a Docker image:
   - `cat websites.txt | docker run -i tpimage`

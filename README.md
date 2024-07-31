# AI User Group Workshop 

## Project set up instructions 

### Python development environment
* VSCode is the preferred IDE.
* Python (minimum version 3.9). 
* Create a Python virtual environment (recommended). [resource](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
  * `python -m venv .venv`
  * `source .venv/bin/activate`
* Create a `.env` file to store your OPENAI Key
  * Navigate to your project's root folder and run the following: `touch .env`, this creates a `.env` file.
  * Add your OPEN API Key to it:
  * `OPENAI_API_KEY = "Your API key goes here"`
* Install the project's required packages. [resource](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-a-requirements-file)
  * `pip install -r requirements.txt`
* Remove the `install==1.3.5` from the "requirement.txt" file as it doesn't resolve to a known package and throws an error during installation. 

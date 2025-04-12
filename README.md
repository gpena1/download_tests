# Using this utility
Make sure this script has the correct permissions before running as an executable. You will also need the directory where the repository is downloaded to stored in the variable `DOWNLOAD_TESTS_DIR`; you can create your own variables file and source this, or simply add it as a global environment variable. You will also need variables for login depending on the judge (for example, CSES requires the variables `CSES_USER` and `CSES_PASSWORD` to have been defined in the environment), so set these accordingly.

Since functionality for CSES uses `cses.py`, you *will* need python installed. If you've looked at the script, you may notice a directory `.venv` being referenced. This is a virtual environment made with Python 3.13.2. The list of dependencies can be found in `requirements.txt`, and can be installed using `pip install -r requirements.txt` after `cd`ing into the repository's directory.

Do be mindful of the fact that this script *will* try to execute with zsh as per the shebang. **Pull requests that modify the shebang will not be accepted.**
# Supported Archives
So far, the script only supports downloading test data from **Kattis** and **CSES**. Whenever you enter any archive names, please enter it in lowercase. If you would like to contribute code that supports other problem archives, make a pull request. Any auxiliary files which serve as aids should be titled with the name of that problem archive (e.g. in order to implement functionality for CSES, I wrote a python script titled `cses.py` to make my life easier).

# Welcome to "Wordall"
For the purpose of excercising my Python knowledge, and for fun, I implemented a version of a popular word guessing game. 

## Setup
### Pre Requisites
1. Install [Git](https://github.com/orgs/community/discussions/135543#discussioncomment-10316669) if you have not already done so
2. Execution of this code requires the installation of [Python 3.11](https://realpython.com/installing-python/) at a minimum.
3. In order to load some of the packages needed, you will also need to install [PIP](https://pip.pypa.io/en/stable/installation/)
4. Finally you will need to install [UV](https://pypi.org/project/uv/)

### Installation
* After ensuring that Python and pip are installed, install UV via pip
```commandline
python3 pip install uv
```
* Download the source to your local environment
```commandline
git clone git@github.com:scottmatth/wordle-clone.git
```
* Navigate to the top level of the cloned repository
* Create and begin a virtual enviornment
```commandline
python3 -m venv .venv
source .venv/bin/activate
```
* Build the repository for wordall
```commandline
uv build
```
* Now you can run the script since all dependencies have not been installed
```commandline
uv run main.py
```
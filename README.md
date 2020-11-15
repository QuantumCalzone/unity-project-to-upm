# unity-project-to-upm
An automation tool to convert your unity project into a package hosted with git.

## How to install
* Open your OS Terminal
* Change your directory to your target Unity project```cd PathToYourUnityProject```
* Add this repo as a submodule```git submodule add https://github.com/QuantumCalzone/unity-project-to-upm```
* Create a virtual environment for by in terminal entering the following ```python3 -m venv PathToProject\unity-project-to-upm\venv```
* Change your directory to your submodule```cd unity-project-to-upm```
* Activate the virtual enviroment```.\env\Scripts\activate``` 
* Install the required packages```python setup.py install```
* Install this package ```pip install git+https://github.com/QuantumCalzone/pythonutils.git```
* Create a shortcut for ```convert_to_upm.py``` (found under unity-project-to-upm) and place it in your desired convenient place

Double click that shortcut when you want to create and push a new version of your package.

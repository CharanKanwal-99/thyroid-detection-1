from setuptools import setup, find_packages
from Typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(path:str)->List[str]:
    """
    Returns all the required packages
    """
    requirements = []
    with open(path) as file:
        requirements = file.readlines()
        requirements = [req.replace("/n", "") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements




setup(
    name = 'Thyroid Detection',
    version='0.0.1'
    author = 'Charan Pandher',
    author_email='charankanwal99@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements(requirements.txt)
)

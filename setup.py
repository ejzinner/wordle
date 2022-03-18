from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Wordle'
LONG_DESCRIPTION = 'Game logic for wordle as well as an algorithm to play wordle'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="wordle", 
        version=VERSION,
        author="Evan Zinner",
        author_email="<ejzinner@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
)
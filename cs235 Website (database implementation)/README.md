# COMPSCI 235 Starter Repository for Assignment 2
This is a starter repository for the assignment 2 of CompSci 235 in Semester 2, 2022.


## Description

This repository contains an implementation of the domain model from Assignment 1. It contains unit tests which can be run through pytest. It also contains a simple Flask application that renders content of a Track object instance from our domain model on a blank html page.

Please note that this sample implementation from Assignment 1 contains a more comprehensive superset of tests compared with what we had as hidden tests on Coderunner. Your domain model implementation may have to be extended to meet all test cases in the sample implementation, but you may also decide to remove or modify test cases as it suits you. 

From here on you can **choose if you want to use the provided domain model or your own implementation from assignment 1**, just make sure your chosen set of test cases always work with your implementation.

## Installation

**Installation via requirements.txt**

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

 
## Data sources

The data files are modified excerpts downloaded from:
https://www.loc.gov/item/2018655052  or
https://github.com/mdeff/fma 

We would like to acknowledge the authors of these papers for introducing the Free Music Archive (FMA), an open and easily accessible dataset of music collections: 

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A Dataset for Music Analysis. In 18th International Society for Music Information Retrieval Conference (ISMIR).

Defferrard, M., Mohanty, S., Carroll, S., & Salathe, M. (2018). Learning to Recognize Musical Genre from Audio. In The 2018 Web Conference Companion. ACM Press.

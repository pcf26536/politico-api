# politico-api
[![Build Status](https://travis-ci.com/wainainad60/politico-api.svg?branch=develop)](https://travis-ci.com/wainainad60/politico-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/09ac0b6bb9682e362053/maintainability)](https://codeclimate.com/github/wainainad60/politico-api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/09ac0b6bb9682e362053/test_coverage)](https://codeclimate.com/github/wainainad60/politico-api/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/wainainad60/politico-api/badge.svg?branch=master)](https://coveralls.io/github/wainainad60/politico-api?branch=master)

This repository holds the API endpoints for politico application. Politico enables citizens give their mandate to politicians running for different government offices while building trust in the process through transparency.

## Requirements
# Install this requirements
- [Git Version Control](https://git-scm.com/)
- [Python 3.6](https://www.python.org/)

<details><summary>Installation</summary>
<p>

#### installation steps

- clone the git repo
```
$ git clone --branch develop https://github.com/wainainad60/politico-api.git
```
- cd into the project directory
```
$ cd politico-api
```
- create the virtual environment and activate it
```
(Linux and Mac OS X)
$ python3 -m venv env 
$ source env/bin/activate

(Windows)
> python -m venv env 
> env\Scripts\activate
```
- install dependencies
```
$ pip install -r requirements.txt
```
- Run the app
``` $ flask run ```

# How to Test the Application
------------------------------------------------------------------
## How to run the unit tests
 On your terminal execute the following command
 
 ```
 $ pytest --cov=api api/tests/ver1/ -v
 ```

# Testing The API Endpoints
Use any API Test Client of choice

I used Postman, get it here => [Postman](https://www.getpostman.com/downloads/)


</p>
</details>

<p></p>
<p></p>

| **API Endpoint** | **Function** | **URL Route** |
| --- | --- | --- |
| **GET** /offices | Get a specific political office record | `api/v1/offices/<int:office_id>` |
| **GET** /offices | Gets all political offices records | `api/v1/offices/` |
| **POST** /offices | Create a political office. | `/api/v1/offices/` |
| **POST** /parties | Creates a political party | `/api/v1/parties/` |
| **DELETE** /parties/`<party-id>` | Delete a political party | `/api/v1/parties/<int:party-id>` |
| **PATCH** /parties/`<party-id>`/name | Edit the name of a specific political party. | `/api/v1/parties/<int:party-id>/name` |
| **GET** /parties | Gets all political parties | `/api/v1/parties/` |
| **GET** /parties/`<int:party-id>` | Gets a specific political party | `/api/v1/parties/<int:party_id>` |

# Credits
[Andela BootCamp Cycle 37](https://andela.com/)


# Author
 Wainaina Gichuhi, wainainad60 @pcf26535

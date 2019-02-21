# politico-api
[![Build Status](https://travis-ci.com/wainainad60/politico-api.svg?branch=develop)](https://travis-ci.com/wainainad60/politico-api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3b017887aca842e598a1f5d9513cacc8)](https://www.codacy.com/app/wainainad60/politico-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wainainad60/politico-api&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/09ac0b6bb9682e362053/maintainability)](https://codeclimate.com/github/wainainad60/politico-api/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/wainainad60/politico-api/badge.svg?branch=develop)](https://coveralls.io/github/wainainad60/politico-api?branch=develop)

This repository holds the API endpoints for politico application. Politico enables citizens give their mandate to politicians running for different government offices while building trust in the process through transparency.

## Requirements
### Install this requirements
- [Git Version Control](https://git-scm.com/)
- [Python 3.6](https://www.python.org/)
- [Postgres 9.5 or Later](https://www.postgresql.org/download/)

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
- set the enviroment settings
```
FLASK_APP="run.py"

SECRET="jwt-secret-string"

APP_SETTINGS='development'

DATABASE_URL="your db url"
TEST_DATABASE_URL="your test db url"
```

- Run the app
``` $ flask run ```

## How to Test the Application
------------------------------------------------------------------
### How to run the unit tests
 On your terminal execute the following command
 
 ```
 $ pytest --cov=api -v
 ```

### Testing The API Endpoints
Use any API Test Client of choice

I used Postman, get it here => [Postman](https://www.getpostman.com/downloads/)

</p>
</details>

###Version 2 Endpoints

| **API Endpoint**                      | **Function**                                 | **URL Route**                               |
| ---                                   | ---                                          | ---                                         |
| **POST** /auth/signup                 | Allows a user to signup                      | `api/v2/auth/signin`                        |
| **POST** /auth/login                  | Allows a user to login                       | `api/v2/auth/login`                         |
| **POST** /auth/reset                  | Allows a user to reset password              | `api/v2/auth/reset`                         |
| **POST** /offices                     | Create a political office.                   | `/api/v2/offices/`                          |
| **GET** /offices/`<office-id>`        | Get a specific political office record       | `api/v2/offices/<int:office_id>`            |
| **GET** /offices                      | Gets all political offices records           | `api/v2/offices/`                           |
| **DELETE** /offices/`<office-id>`     | Delete a political office                    | `/api/v2/offices/<int:office-id>`           |
| **PATCH** /offices/`<office-id>`/name | Edit the name of a specific political office.| `/api/v2/offices/<int:office-id>/name`      |
| **POST** /parties                     | Creates a political party                    | `/api/v2/parties/`                          |
| **DELETE** /parties/`<party-id>`      | Delete a political party                     | `/api/v2/parties/<int:party-id>`            |
| **PATCH** /parties/`<party-id>`/name  | Edit the name of a specific political party. | `/api/v2/parties/<int:party-id>/name`       |
| **GET** /parties                      | Gets all political parties                   | `/api/v2/parties/`                          |
| **GET** /parties/`<int:party-id>`     | Gets a specific political party              | `/api/v2/parties/<int:party_id>`            |
| **POST** /office/1/register           | Registers a candidate to a political office. | `/api/v2/offices/<int:office-id>/register`  |
| **POST** /votes/                      | Votes for a candidate.                       | `/api/v2/votes/`                            |
| **GET** /office/1/result              | View the votes results of an office.         | `/api/v2/offices/<int:office-id>/result`    |
| **POST** /petitions/                  | Create a petition.                           | `/api/v2/petitions/`                        |

###Version 1 Endpoints

| **API Endpoint**                     | **Function**                                 | **URL Route**                         |
| ---                                  | ---                                          | ---                                   |
| **GET** /offices                     | Get a specific political office record       | `api/v1/offices/<int:office_id>`      |
| **GET** /offices                     | Gets all political offices records           | `api/v1/offices/`                     |
| **POST** /offices                    | Create a political office.                   | `/api/v1/offices/`                    |
| **POST** /parties                    | Creates a political party                    | `/api/v1/parties/`                    |
| **DELETE** /parties/`<party-id>`     | Delete a political party                     | `/api/v1/parties/<int:party-id>`      |
| **PATCH** /parties/`<party-id>`/name | Edit the name of a specific political party. | `/api/v1/parties/<int:party-id>/name` |
| **GET** /parties                     | Gets all political parties                   | `/api/v1/parties/`                    |
| **GET** /parties/`<int:party-id>`    | Gets a specific political party              | `/api/v1/parties/<int:party_id>`      |


## Credits
[Andela BootCamp Cycle 37](https://andela.com/)


## Author
 Wainaina Gichuhi, wainainad60 @pcf26535

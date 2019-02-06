# politico-api
[![Build Status](https://travis-ci.com/wainainad60/politico-api.svg?branch=develop)](https://travis-ci.com/wainainad60/politico-api)

This repository holds the API endpoints for politico application. Politico enables citizens give their mandate to politicians running for different government offices while building trust in the process through transparency.

## Requirements
- [Python 3.x](https://www.python.org/)
- Any text editor or python IDE. Recommended [Visual Studio code](https://code.visualstudio.com/)
- Any API client. Recommended [Postman](https://www.getpostman.com/downloads/)
- Any Operating System. Recommeded Mac OS X, Linux or Windows
- Git version control

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
$ python3 -m venv venv 
$ source venv/bin/activate

(Windows)
> python -m venv venv 
> venv\Scripts\activate
```
- install dependencies
```
$ pip install -r requirements.txt
```
- Run the app
``` $ flask run ```

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
| **PATCH** /parties/`<party-id>`/name | Edit the name of a specific political party. | `/api/v1/parties/<int:party-id>/<string:name>` |
| **GET** /parties | Gets all political parties | `/api/v1/parties/` |
| **GET** /parties/`<int:party-id>` | Gets a specific political party | `/api/v1/parties/<int:party_id>` |

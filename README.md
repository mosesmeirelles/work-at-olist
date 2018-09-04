# Phone Bills API - Olist

[![Build Status](https://travis-ci.org/moshemeirelles/work-at-olist.svg?branch=master)](https://travis-ci.org/moshemeirelles/work-at-olist)

This repository contains a problem used to evaluate the candidate skills to Olist Challenge. It implements an REST API application that receives call detail records and calculates monthly bills for a given telephone number. It uses part of concept of Domain Driven Design, respecting domains to encapsulate business logic. It has the following features:

- Users can Insert, Update, Retrieve and Delete Call Records
- Users can Insert, Update, Retrieve and Delete Tariff to configure call prices and intervals
- Users can get bill price to specific period

The project is live running and can be acessed at [Heroku](https://phonebills.herokuapp.com/)

### How to develop

1. Clone project
2. Move to project folder
3. Start virtual env
4. Install dependencies
5. Run migrations

```
git clone https://github.com/moshemeirelles/work-at-olist.git
cd work-at-olist
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python manage.py migrate
```

### Testing

1. To test, install some fixtures from project folder
2. Execute tests

```
python manage.py loaddata fixtures/*.json
python manage.py test
```
    
## Work Environment

- Notebook Dell Vostro 3550
- OS Ubuntu 16.04
- IDE PyCharm

### Resources
- Django 2.1
- Django Rest Framework 3.8
- Model Mommy 1.6 (Unit Testing)
- Database PostgreSQL

## Endpoints

Full documentation can be acessed at [docs on Heroku](https://phonebills.herokuapp.com/docs/)

**Call Record Resources**

* `GET` callrecord
* `POST` callrecord
* `GET` callrecord/:id
* `PUT` callrecord/:id
* `DELETE` callrecord/:id

**Tariff Resources**

* `GET` tariff
* `POST` tariff
* `GET` tariff/:id
* `PUT` tariff/:id
* `DELETE` tariff/:id

**Phone Bill Resources**

* `GET` bill/:phone_number (optional query params: month & year)


## Notes

### Questions

- Commits pattern is correct?
- Update a call record is a security failure?
- Is possible to have call on same time for same source/destination?


### Improvements

- implement calculations using tariff to reduced time (ignored today considering value zero)

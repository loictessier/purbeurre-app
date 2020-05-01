# purbeurre-app

Purbeurre is a Django application whose concept is to offer the users the possibility of looking for healthy substitutes for everyday products. This project is part of a learning path "Python application developper" which you can find on OpenClassrooms web site.

## Structure

this project contains several apps :
- **core** : the base components
- **favorite** : handle the feature that allows users to add products to their favorites list
- **openFoodFacts** : handle the products views, models, and scripts to populate database
- **user** : handle signup and authentication

## Tests

To run the tests install the packages with pipenv then starts shell

```
pipenv install
pipenv shell
```

Then you can run the tests :

```
python manage.py test
```

Use the coverage tool :

```
coverage run --source='.' manage.py test
coverage html
```

To run the functional test script :

```
python functional_tests.py
```
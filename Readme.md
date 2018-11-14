Find a vegetal alternative to animal food products. Based on [Open Food Facts](https://fr.openfoodfacts.org) data and Django.

# Vegalt-Django

This project is the follower of https://github.com/MaevaBrunelles/vegalt (OC-P5). So, what's new ?

* Based on Django
* Online application
* Account creation
 
Vegalt-Django is currently available in French :fr:.

## Utilisation

### Online application

Just click here : https://vegalt-oc.herokuapp.com/ and enjoy it !

### From sources

#### Clone the project

```sh
git clone git://github.com/MaevaBrunelles/vegalt-django
```

#### Install librairies

Vegalt-Django needs external librairies to work, including of course :

* [Django](https://github.com/django/django) - The Web framework for perfectionists with deadlines


You can easily install all of the required librairies with the following command :

```sh
$ python3 install -r requirements.txt
```

#### Launch the application

```sh
$ ./manage.py runserver
```

This will launch Django server. You can visit localhost at https://127.0.0.1:8000/, and enjoy it !

## Examples of available products

You can currently search alternatives for thoses products :

* Steak :fr:
* Lait :fr:
* Yaourt :fr:
* Crème :fr:
* Saucisse :fr:
* Jambon :fr:

To be complete...

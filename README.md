# Walletsaver - Tech assignment

Hello!
This is a nice challenge. And I mean even without the frontend!
I'll separate in sections, to better explain each development stage.


# Development process

## Environment

I use `pyenv`, it's very cool to be able to have several python versions available. And with the plugin `pyenv-virtualenv`, even the virtualenvs are taken care of.

So, I'll use python `3.6.5`, as the new `3.7` isn't available in pyenv yet.

This is what I did:

```bash
$ pyenv install 3.6.5
$ pyenv virtualenv 3.6.5 wsaver
$ cd <project-dir>
$ pyenv local wsaver
$ pip install -U pip
$ pip install -r requirements.txt
```

## Scraping

I've never scraped a site before.
After a few hours researching, I've found several alternatives like scrapy, lxml and beautifulsoup.

Scrapy seems to be a good choice for a company which does a lot of website crawling. It manages to provide a full ecosystem to fetch, process and persist data, as well as standardize tools like scrapyd to host "spyders" and a command line to easy deploy them.

The others seemed better to what I needed here. They're not a full blown system, they're frameworks. Both seemed ok, but I liked the beautifulsoup interface better (and I hate xml, would never pick the other anyway).
So, I've chosen beautifulsoup, as it seemed very easy to use.

The [https://www.fastweb.it](https://www.fastweb.it) page I needed to extract data from was very weird, at least to me, with untrained frontend eyes, with a bunch of spams intertwined together, with parts of text split in several of them.

But fortunately they weren't that hard to extract, I've initially made an imperative algorithm using for loops, but as I'm using a modern Python 3, I've challenged myself to do it in a functional style, using only iterators. It came out very neat and pythonic.

### Note: data synchronization and handling

In an actual production system, there would be another important part: updating these data seamlessly. The data already captured should be synchronized from time to time with the live one on the source site, minimizing dirty reads and downtime.
I would set up an asynchronous task handler like celery to run this task regularly, like once or twice a day.

To not ever removing data, as customers would probably have already chosen some of them, it would be necessary some versioning or expiry control, to be able to retrieve only current plans, without losing any history.

Another consideration would be internationalization. The extracted data are in Italian, which may be fine for an italian company, with a customer base in Italy. But since the company is going to be global, there should be some way to translate these content.

## Web framework

I'll use Django, no doubt about it. I love Django.

Only I don't know the new Django 2.0, but it's a great opportunity to get to try it! :)

## Database

PostgreSQL is an easy choice too. Excellent database, and one I've already worked with.

## Docker infrastructure

Nowadays it's the best way to set up complex applications, without falling in dependency hell.
I'll use `docker-compose` to get an up and running database, and maybe a Dockerfile at the end, for an easy deployment.

## REST API

This were a tough one. There's the famous Django Rest Framework, which I don't like, and alternatives like the also famous Restless and Tastypie, or the bleeding edge API Star.

The DRF framework is complete, including an API browser, but I've always found it very convoluted. It tries to be so flexible that the usability suffers. But it is good nevertheless.

## Tests

For this project, I've decided to experiment leaving the tests out of the python source code. This means the packaging process can get only actual code, and test code never gets to the production environment. The biggest advantage of this is eliminating the risk of importing and running them there, which could wreak havok in the db.

I had to include a new dependency `pytest-pythonpath` and create a `pytest.ini` to get the django settings to be found.

Actually, when I got to the point of testing a django model, I've included the `factory-boy` dependency, and I've realized I couldn't import my new `modelfactory` in shell_plus...
I undid the split tests from the source. 

To achieve again that production obliterate of tests, the `Dockerfile` recipe would have to delete the tests files, which is doable, but harder.

## Deploy

## Frontend

# How to use

## Initialize data

Enter the `manage.py` directory and run:

```bash
$ ./manage.py shell_plus
```

Now fetch the fastweb data and should obtain:

````python
In [1]: CarrierPlan.objects.resync_plans(1)

In [2]: CarrierPlan.objects.all()
Out[2]: <CarrierPlanQuerySet [<CarrierPlan: #1 fastweb:INTERNET>, <CarrierPlan: #2 fastweb:INTERNET + TELEFONO>, <CarrierPlan: #3 fastweb:INTERNET e Sky>, <CarrierPlan: #4 fastweb:INTERNET + TELEFONO e Sky>, <CarrierPlan: #5 fastweb:INTERNET + ENERGIA>, <CarrierPlan: #6 fastweb:INTERNET + TELEFONO + ENERGIA>]>
````

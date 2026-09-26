# Bangladesh District & Upazila Seed Data for Django

A reusable Django management command for creating Bangladesh district and upazila data in a Django project.

This repository provides a simple way to add district and upazila data to a Django database without manually entering the locations one by one.

## Features

* Bangladesh district data
* Bangladesh upazila data
* Django management command
* Duplicate-safe data insertion
* Easy copy-and-use setup
* Suitable for Django projects that need Bangladesh location data

## Requirements

* Python 3.10+
* Django 4.2+
* A Django project
* `District` and `Upazila` models

## Installation

You do not need to install this repository as a Python package.

Simply copy the `management` folder from this repository into the Django app that contains your `District` and `Upazila` models.

Your Django app should look similar to this:

```text
your_project/
│
├── manage.py
│
└── your_app/
    ├── models.py
    │
    ├── management/
    │   ├── __init__.py
    │   └── commands/
    │       ├── __init__.py
    │       └── seed_locations.py
    │
    └── views.py
```

## 1. Copy the management folder

Copy the `management` folder from this repository:

```text
management/
├── __init__.py
└── commands/
    ├── __init__.py
    └── seed_locations.py
```

Paste it inside the Django app where your `District` and `Upazila` models are located.

For example:

```text
your_project/
│
└── core/
    ├── models.py
    │
    └── management/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── seed_locations.py
```

## 2. Check the model import

The included `seed_locations.py` uses:

```python
from core.models import District, Upazila
```

In this repository, `core` is used as the example Django app name.

If your `District` and `Upazila` models are located in another app, update the import according to your project.

For example, if your app is named `food`:

```python
from food.models import District, Upazila
```

If your app is named `locations`:

```python
from locations.models import District, Upazila
```

## 3. Make sure your models exist

The management command expects models similar to:

```python
class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Upazila(models.Model):
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="upazilas"
    )
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["district", "name"],
                name="unique_upazila_per_district"
            )
        ]

    def __str__(self):
        return self.name
```

Your models do not have to be exactly the same, but the field names and relationships used by `seed_locations.py` must match your models.

## 4. Make sure the Django app is installed

The app containing the `management` folder must be included in `INSTALLED_APPS` in your Django settings.

For example:

```python
INSTALLED_APPS = [
    ...
    "core",
]
```

If your app has a different name, use that app name instead.

## 5. Run migrations

After creating or updating your models, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Run the seed command

Run:

```bash
python manage.py seed_locations
```

The command will create the district and upazila records in your database.

## Project Structure Example

A complete example may look like:

```text
your_project/
│
├── manage.py
│
├── your_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── core/
    ├── models.py
    ├── views.py
    │
    └── management/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── seed_locations.py
```

## Important

This repository contains the reusable Django management command, not a complete Django project.

You are responsible for:

* Creating your own Django project
* Creating the `District` and `Upazila` models
* Running migrations
* Making sure the app is included in `INSTALLED_APPS`
* Updating the model import in `seed_locations.py` if necessary
* Updating views, forms, serializers, URLs, or other project-specific code according to your own project structure

## Data Status

Bangladesh's administrative structure can change over time.

District and upazila names or administrative boundaries may be changed by the relevant authorities. Always verify the current administrative information against official Bangladesh government sources before using the data in a production application.

## License

The code in this repository is released under the MIT License.

The MIT License applies to the code in this repository. Administrative data may have separate provenance or usage considerations, so users should verify the applicable official sources and terms when redistributing or using the data.

## Contributing

Corrections and improvements are welcome.

If you find an incorrect or outdated district or upazila entry, please provide a reliable official source when submitting an issue or pull request.

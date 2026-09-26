# Bangladesh District & Upazila Seed Data for Django

A reusable Django management command for creating Bangladesh district and upazila data in your Django project.

## What is included

This repository provides:

* Bangladesh district data
* Bangladesh upazila data
* Django management command for seeding the data
* Simple copy-and-use setup
* Duplicate-safe database insertion

## Requirements

* Python 3.10+
* Django 4.2+
* A Django project with `District` and `Upazila` models

## Installation

You do not need to install this repository as a Python package.

Simply copy the `management` folder from this repository into the Django app that contains your `District` and `Upazila` models.

Your app structure should look like this:

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

Copy:

```text
management/
└── commands/
    └── seed_locations.py
```

into the Django app where your `District` and `Upazila` models are located.

For example:

```text
your_app/
├── models.py
└── management/
    └── commands/
        └── seed_locations.py
```

## 2. Check the model import

Open:

```text
management/commands/seed_locations.py
```

Find the model import.

For example:

```python
from your_app.models import District, Upazila
```

Replace `your_app` with the actual Django app name containing your models.

For example, if your app is named `core`:

```python
from core.models import District, Upazila
```

If your app is named `food`:

```python
from food.models import District, Upazila
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

Your existing models may use different field names. In that case, update `seed_locations.py` accordingly.

## 4. Run migrations

After creating or updating your models:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Run the seed command

Run:

```bash
python manage.py seed_locations
```

The command will create the district and upazila records in your database.

## Django app structure

Make sure the app containing the management command is included in:

```python
INSTALLED_APPS
```

in your Django settings.

For example:

```python
INSTALLED_APPS = [
    ...
    "your_app",
]
```

## Important

This repository contains the reusable management command, not a complete Django project.

You are responsible for:

* Creating the Django project
* Creating the `District` and `Upazila` models
* Running migrations
* Updating model imports
* Updating views, serializers, forms, or URLs according to your own project structure

## Data source

Bangladesh's administrative structure can change over time. Always verify district and upazila names against current official Bangladesh government sources before using the data in a production application.

## License

The code in this repository is released under the MIT License.

The MIT License applies to the code in this repository. Administrative data may have separate provenance or usage considerations, so verify the applicable official sources and terms when redistributing or using the data.

## Contributing

Pull requests and corrections are welcome.

If an administrative name or structure changes, please provide a reliable official source with the proposed update.

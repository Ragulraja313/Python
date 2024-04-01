from django.db import models


class Books(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.name


class MyModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    Domain = models.CharField(max_length=100, default="Python")
    Age = models.IntegerField(default=0)
    Language = models.CharField(max_length=50, default="Tamil")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title

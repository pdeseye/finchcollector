from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS = (
  ('S', 'Seed'),
  ('W', 'Worm'),
  ('D', 'Drink')
)


class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('toys_detail', kwargs={'pk': self.id})

class Finch(models.Model):
  name = models.CharField(max_length=100)
  sex = models.CharField(max_length=20)
  description = models.TextField(max_length=250)
  color = models.CharField(max_length=30)
  toys = models.ManyToManyField(Toy)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def fed_for_today(self):
    return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

  def __str__(self):
    return self.name


  def get_absolute_url(self):
    return reverse('finches_detail', kwargs={'finch_id': self.id})

class Feeding(models.Model):
  date = models.DateField('Feeding date')
  meal = models.CharField(
		max_length=1,
		choices=MEALS,
		default=MEALS[0][0]
  )
  # Create a cat_id column in the database
  finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_meal_display()} on {self.date}"

  class Meta:
    ordering = ['-date']

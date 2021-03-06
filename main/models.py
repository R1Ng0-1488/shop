from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name 

	def get_absolute_url(self):
		return reverse('main:product_list_by_category', args=[self.slug])


class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='producte')
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True)
	image = models.URLField(blank=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=0)
	stock = models.PositiveIntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)

	def __str__(self):
		return self.name 

	def get_absolute_url(self):
		return reverse('main:product_detail', args=[self.id, self.slug])
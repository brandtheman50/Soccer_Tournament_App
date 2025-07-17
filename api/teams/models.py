from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # prevents Django from creating a table

class Team(BaseModel):
    name = models.CharField(max_length=100)
    coach_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=25)
    contact_email = models.CharField(max_length=50)

class Player(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=25)
    contact_email = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    date_of_birth = models.DateField()
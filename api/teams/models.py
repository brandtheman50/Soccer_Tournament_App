from django.db import models
from users.models import User

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # prevents Django from creating a table

class Team(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PlayerProfile(BaseModel):
    date_of_birth = models.DateField()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class TeamMembership(BaseModel):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('player', 'Player'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_users")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_membership")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Renamed property easier read
    @property 
    def joined_at(self):
        return self.created_at
    
    class Meta:
        unique_together = ('user', 'team')  # optional
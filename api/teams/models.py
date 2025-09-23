from django.db import models
from users.models import User

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # prevents Django from creating a table

class Team(BaseModel):
    name = models.CharField(max_length=50)
    logo_file_path = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PlayerProfile(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    profile_photo = models.CharField(null=False, blank=False, max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "email"],
                name="uniq_player_email_per_team"
            )
        ]
    
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
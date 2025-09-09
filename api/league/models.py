from django.db import models
from teams.models import Team, BaseModel

# Create your models here.

class League(BaseModel):
    name = models.CharField(max_length=50)

class TeamStanding(BaseModel):
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="team_standings")
    league = models.ForeignKey(League, on_delete=models.PROTECT, related_name="standings")

    matches_played = models.PositiveSmallIntegerField(default=0)
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    draws = models.PositiveSmallIntegerField(default=0)

    goals_for = models.PositiveSmallIntegerField(default=0)
    goals_against = models.PositiveSmallIntegerField(default=0)

    @property
    def points(self):
        return self.wins * 3 + self.draws
    
    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against
    
    class Meta:
        unique_together = ('team', 'league')


class Match(BaseModel):
    league = models.ForeignKey(League, on_delete=models.PROTECT, related_name="matches")
    home_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="away_matches")
    field_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    scheduled_date = models.DateTimeField()
    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"
    
    def get_winner(self):
        if self.home_score > self.away_score:
            return self.home_team.name
        elif self.home_score < self.away_score:
            return self.away_team.name
        else:
            return "Draw"
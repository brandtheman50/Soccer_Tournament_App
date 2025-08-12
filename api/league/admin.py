from django.contrib import admin
from .models import Match, TeamStanding, League

class MatchInline(admin.StackedInline):
    model = Match
    extra = 0
    ordering = ('-scheduled_date', '-id')
    fields = ('scheduled_date', 'league', 'home_team', 'away_team', 'field_name', 'address', 'home_score', 'away_score')

@admin.register(TeamStanding)
class TeamStandingAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'league', 'matches_played', 'wins', 'losses', 'draws', 'goals_for', 'goals_against', 'created_at', 'updated_at')
    ordering = ('-id',)
    search_fields = ['id', 'team__name', 'league__name']

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('-id',)
    search_fields = ['id', 'name']
    inlines = [MatchInline]
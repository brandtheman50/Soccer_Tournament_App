from ..models import Match, TeamStanding

def rollback_standings(match: Match):

    home_score = match.home_score
    away_score = match.away_score

    if home_score is None or away_score is None:
        return
    
    home_team = match.home_team
    away_team = match.away_team
    league = match.league

    # Reverse the previously applied standings effect
    home_standing = TeamStanding.objects.get(team=home_team, league=league)
    away_standing = TeamStanding.objects.get(team=away_team, league=league)

    home_standing.matches_played -= 1
    away_standing.matches_played -= 1

    home_standing.goals_for -= home_score
    home_standing.goals_against -= away_score
    away_standing.goals_for -= away_score
    away_standing.goals_against -= home_score

    # Reverse result
    if home_score > away_score:
        home_standing.wins -= 1
        away_standing.losses -= 1
    elif home_score < away_score:
        home_standing.losses -= 1
        away_standing.wins -= 1
    else:
        home_standing.draws -= 1
        away_standing.draws -= 1

    home_standing.save()
    away_standing.save()


def update_standings_for_match(match: Match):

    # Rollback previous standings if applied

    # Apply new standings
    home_team = match.home_team
    away_team = match.away_team
    home_score = match.home_score
    away_score = match.away_score

    if home_score is None or away_score is None:
        return # Don't update for incomplete matches

    try:
        home_standings = TeamStanding.objects.get(team=home_team, league=match.league)
        away_standings = TeamStanding.objects.get(team=away_team, league=match.league)
    except TeamStanding.DoesNotExist:
        raise ValueError("TeamStanding missing for one of the teams in this match.")

    home_standings.matches_played += 1
    away_standings.matches_played += 1

    # Compute results
    if home_score > away_score:
        home_standings.wins += 1
        away_standings.losses += 1
    elif home_score < away_score:
        home_standings.losses += 1
        away_standings.wins += 1
    else:
        home_standings.draws += 1
        away_standings.draws += 1
    
    home_standings.goals_for += match.home_score
    away_standings.goals_for += match.away_score

    home_standings.goals_against += match.away_score
    away_standings.goals_against += match.home_score

    home_standings.save()
    away_standings.save()
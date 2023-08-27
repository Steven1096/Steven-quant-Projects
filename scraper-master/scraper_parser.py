#coding: utf-8
"""
    scrapper_parser.py
"""

import bs4


def parse_opponent_name(node, away_team=False):
    """
        Parse opponent name from data.
    """
    team_class = 'awayTeam' if away_team else 'homeTeam'
    return node.find('div', {'itemprop': team_class}).find('p').text


def parse_score(node):
    """
        Parse score from data
    """
    home, away = node.find('div', {'class': 'scoreline'}).find('span').text\
                 .strip().split('-')
    return int(home), int(away)


def parse_teams_results(data):
    """
        Parse teams results from data.
    """
    beautiful_soup = bs4.BeautifulSoup(data, 'html.parser')
    match_history_events = filter(
        lambda x: 'incomplete' not in x['class'],
        beautiful_soup.find_all('li', {'class' : 'matchHistoryEvent'}))

    return list(map(
        lambda x: {'home': parse_opponent_name(x, 0),
                   'visitor': parse_opponent_name(x, True),
                   'score': parse_score(x)},
        match_history_events))


def parse_teams(data):
    """
        Parse teams urls from data.
    """
    beautiful_soup = bs4.BeautifulSoup(data, 'html.parser')
    return [
        {'name': x.text, 'url': x['href']} for x in beautiful_soup.find_all(
            'a', {'class' : 'bold hover-modal-parent hover-modal-ajax-team'})]

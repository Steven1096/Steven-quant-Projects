#coding: utf-8
"""
    App.py
"""

import json
import logging
import time
import requests
import scraper_parser as sp


def http_get(url, retry=10):
    """
        Wrapper on request.get.
    """
    sleep_time = 1
    while retry > 0:
        req = requests.get(url)
        if req.status_code == 200 and len(req.content) != 0:
            return req
        retry -= 1
        logging.error('GET %s failed, response code = %d,'\
                      'content length = %d, retry = %d, sleep = %ds',
                      url, req.status_code, len(req.content), retry, sleep_time)
        time.sleep(sleep_time)
        sleep_time *= 2
    raise RuntimeError('HTTP Get {} failed.'.format(url))


def is_team_candidate(team_results):
    """
        Check if a team met our criterias based on its previous results.
    """
    for result in team_results[:5]:
        if sum(result['score']) in (2, 3):
            return False
    return True


def main():
    """
        Main function.
    """
    with open('conf.json', 'r') as conf_file:
        conf = json.load(conf_file)

    root_url = conf['root_url']
    output_file = conf['output_file']
    leagues = conf['leagues']
    logging.info('Configuration loaded!')

    result = 'league, team, is_candidate\n'
    for ligue in leagues:
        logging.info('League -> %s.', ligue)
        for team in sp.parse_teams(http_get(root_url + ligue).content):
            logging.info('Team -> %s.', team['name'])
            team_results = sp.parse_teams_results(
                http_get(root_url + team['url']).content)
            result += '{}, {}, {}\n'.format(
                ligue, team['name'],
                'yes' if is_team_candidate(team_results) else 'no')
            with open(output_file, 'a') as result_file:
                result_file.write(result)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
        main()
    except RuntimeError as msg:
        logging.error(msg)

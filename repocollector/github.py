"""
A module to mine Github to extract relevant repositories based on given criteria
"""

import re
import requests
from datetime import datetime

QUERY_TEMPLATE = """{ search(query: "is:public stars:>=MIN_STARS mirror:false archived:false created:SINCE..UNTIL 
pushed:>=PUSHED_AFTER LANGUAGE:LANGUAGE", type: REPOSITORY, first: 50 AFTER) { repositoryCount pageInfo { endCursor startCursor 
hasNextPage } edges { node { ... on Repository { databaseId defaultBranchRef { name } owner { login } name url description 
primaryLanguage { name } stargazers { totalCount } watchers { totalCount } releases { totalCount } issues { 
totalCount } createdAt pushedAt updatedAt hasIssuesEnabled isArchived isDisabled isMirror isFork object(expression: 
"master:") { ... on Tree { entries { name type } } } } } } } 

    rateLimit {
        limit
        cost
        remaining
        resetAt
    }
}
"""


class GithubRepositoriesCollector:

    def __init__(self, access_token):
        """
        Crawl GitHub to extract repositories

        :param access_token: the token to query GraphQL (https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
        """

        self._token = access_token
        self._quota = 0
        self._quota_reset_at = None

    @property
    def quota(self):
        return self._quota

    @property
    def quota_reset_at(self):
        return self._quota_reset_at

    @staticmethod
    def filter_repositories(edges,
                            min_issues: int = 0,
                            min_releases: int = 0,
                            min_watchers: int = 0):

        for node in edges:

            node = node.get('node')

            if not node:
                continue

            has_issues_enabled = node.get('hasIssuesEnabled', True)
            issues = node['issues']['totalCount'] if node['issues'] else 0
            releases = node['releases']['totalCount'] if node['releases'] else 0
            stars = node['stargazers']['totalCount'] if node['stargazers'] else 0
            watchers = node['watchers']['totalCount'] if node['watchers'] else 0
            is_disabled = node.get('isDisabled', False)
            is_fork = node.get('isFork', False)
            is_locked = node.get('isLocked', False)
            is_template = node.get('isTemplate', False)
            primary_language = node['primaryLanguage']['name'].lower() if node['primaryLanguage'] else ''

            if min_issues and not has_issues_enabled:
                continue

            if issues < min_issues:
                continue

            if releases < min_releases:
                continue

            if watchers < min_watchers:
                continue

            if is_disabled or is_locked or is_template:
                continue

            if is_fork:
                continue

            object = node.get('object')
            if not object:
                continue

            dirs = [entry.get('name') for entry in object.get('entries', []) if entry.get('type') == 'tree']

            owner = node.get('owner', {}).get('login', '')
            name = node.get('name', '')

            print(node)

            yield dict(
                id=node.get('databaseId'),
                default_branch=node.get('defaultBranchRef', {}).get('name'),
                owner=owner,
                name=name,
                full_name=f'{owner}/{name}',
                url=node.get('url'),
                description=node['description'] if node['description'] else '',
                issues=issues,
                releases=releases,
                stars=stars,
                watchers=watchers,
                primary_language=primary_language,
                created_at=str(node.get('createdAt')),
                pushed_at=str(node.get('pushedAt')),
                dirs=dirs
            )

    def collect_repositories(self,
                             since: datetime,
                             until: datetime,
                             pushed_after: datetime,
                             min_stars: int = 0,
                             min_releases: int = 0,
                             min_watchers: int = 0,
                             min_issues: int = 0,
                             primary_language: str = None):
        """
        :param since: search for repositories created from since
        :param until: search for repositories created up to until
        :param pushed_after: datetime to filter out repositories. Repositories older than pushed_after are ignored.
        :param min_stars: the minimum number of stars the repositories must have
        :param min_releases: the minimum number of releases the repositories must have
        :param min_watchers: the minimum number of watchers the repositories must have
        :param min_issues: the minimum number of issues the repositories must have
        :param primary_language: get repositories written in this language

        :return: a generator of dictionary objects
        """

        query = re.sub('MIN_STARS', str(min_stars), QUERY_TEMPLATE)
        query = re.sub('SINCE', since.strftime('%Y-%m-%dT%H:%M:%SZ'), query)
        query = re.sub('UNTIL', until.strftime('%Y-%m-%dT%H:%M:%SZ'), query)
        query = re.sub('PUSHED_AFTER', pushed_after.strftime('%Y-%m-%dT%H:%M:%SZ'), query)

        if primary_language:
            query = re.sub('LANGUAGE:LANGUAGE', f'language:{primary_language}', query)
        else:
            query = re.sub('LANGUAGE:LANGUAGE', '', query)

        has_next_page = True
        end_cursor = None

        while has_next_page:

            tmp_query = re.sub('AFTER', '', query) if not end_cursor else re.sub('AFTER',
                                                                                 f', after: "{end_cursor}"',
                                                                                 query)

            response = requests.post('https://api.github.com/graphql', json={'query': tmp_query},
                                     headers={'Authorization': f'token {self._token}'})

            if response.status_code != 200:
                print("Query failed to run and returned status code {}: {}".format(response.status_code, tmp_query))
                break

            query_result = response.json()

            if not query_result.get('data'):
                break

            if not query_result['data'].get('search'):
                break

            self._quota = int(query_result['data']['rateLimit']['remaining'])
            self._quota_reset_at = query_result['data']['rateLimit']['resetAt']

            has_next_page = bool(query_result['data']['search']['pageInfo'].get('hasNextPage'))
            end_cursor = str(query_result['data']['search']['pageInfo'].get('endCursor'))

            edges = query_result['data']['search'].get('edges', [])

            for repo in self.filter_repositories(edges,
                                                 min_issues=min_issues,
                                                 min_releases=min_releases,
                                                 min_watchers=min_watchers):
                yield repo

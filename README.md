# radon-repositories-collector
A Python package to query GraphQL for collecting GitHub repositories metadata.

![lgtm](https://img.shields.io/lgtm/grade/python/github/radon-h2020/radon-repositories-collector)
![pypi-version](https://img.shields.io/pypi/v/repositories-collector)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


Note, the tool requires a personal access token to access the GraphQL APIs. 
See how to get one [here](https://github.com/settings/tokens).

## Install

The package can be installed from [PyPI](https://pypi.org/project/repositories-collector/) as follows:

```pip install repositories-collector```

## Python usage

```python
import os
from datetime import datetime
from repocollector.github import GithubRepositoriesCollector

github_crawler = GithubRepositoriesCollector('<GITHUB ACCESS TOKEN>') 

for repo in github_crawler.collect_repositories(
                since=datetime(2019, 12, 31),
                until=datetime(2020, 12, 31),
                pushed_after=datetime(2020, 6, 1),
                min_issues=0,
                min_releases=0,
                min_stars=0,
                min_watchers=0,
                primary_language='<language>'):

    print('id:', repo['id']) # e.g., 123456
    print('default_branch:', repo['default_branch']) # e.g., main
    print('owner:', repo['owner']) # e.g., radon-h2020
    print('name:', repo['name']) # e.g., radon-repositories-collector
    print('full name:', repo['full_name']) # e.g., radon-h2020/radon-repositories-collector
    print('url:', repo['url'])
    print('description:', repo['description'])
    print('issues:', repo['issues'])
    print('releases:', repo['releases'])
    print('stars:', repo['stars'])
    print('watchers:', repo['watchers'])
    print('primary_language:', repo['primary_language'])
    print('created_at:', repo['created_at'])
    print('pushed_at:', repo['pushed_at'])
    print('dirs:', repo['dirs']) # list of repo's root directories, e.g., [repocollector]
```


## Command-line usage

```
A Python library to collect repositories metadata from GitHub.

positional arguments:
  since                 collect repositories created since this date (default: 2014-01-01 00:00:00)
  until                 collect repositories created up to this date (default: 2014-01-01 00:00:00)
  dest                  destination folder for report

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --pushed-after DATE_PUSH
                        collect only repositories pushed after this date (default: 2014-01-01 00:00:00)
  --min-issues MIN_ISSUES
                        collect repositories with at least <min-issues> issues (default: 0)
  --min-releases MIN_RELEASES
                        collect repositories with at least <min-releases> releases (default: 0)
  --min-stars MIN_STARS
                        collect repositories with at least <min-stars> stars (default: 0)
  --min-watchers MIN_WATCHERS
                        collect repositories with at least <min-watchers> watchers (default: 0)
  --primary-language PRIMARY_LANGUAGE
                        collect repositories written in this language
  --verbose             show log (default: False)

```


**Output**
Running the tool from command-line generates a JSON and HTML report accessible at *\<dest\>/report.html*.



**Example**
The following command searches for repositories written in python created between 31 Dec 2019 and 31 Dec 2020 with at least one commit after 1 Jun 2020 (i.e.,pushed after):

`repositories-collector 2019-12-31 2020-12-31 /tmp/ --pushed_after 2020-06-01 --min_issues 0 --min_releases 0 --min_stars 0 --min_watchers 0 --primary_language python`

The report is saved at `/tmp/repositories.html` and `/tmp/repositories.json`.







![lgtm](https://img.shields.io/lgtm/grade/python/github/radon-h2020/radon-repositories-collector)
![LGTM Alerts](https://img.shields.io/lgtm/alerts/github/radon-h2020/radon-repositories-collector)
![pypi-version](https://img.shields.io/pypi/v/repositories-collector)
![pypi-status](https://img.shields.io/pypi/status/repositories-collector)
![release-date](https://img.shields.io/github/release-date/radon-h2020/radon-repositories-collector)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


# radon-repositories-collector
A Python package to query GraphQL for collecting repositories metadata.


```python
import os
from datetime import datetime
from repocollector import GithubRepositoriesCollector

github_crawler = GithubRepositoriesCollector(
                access_token=os.getenv('GITHUB_ACCESS_TOKEN'),  # or paste your token
                since=datetime(2019, 12, 31),
                until=datetime(2020, 12, 31),
                pushed_after=datetime(2020, 6, 1),
                min_issues=0,
                min_releases=0,
                min_stars=0,
                min_watchers=0)

for repo in github_crawler.collect_repositories():
    print('id:', repo['id']) # e.g., 123456
    print('default_branch:', repo['default_branch']) # e.g., main
    print('owner:', repo['owner']) # e.g., radon-h2020
    print('name:', repo['name']) # e.g., radon-repositories-collector
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



## How to install

The package can be downloaded from [PyPI](https://pypi.org/project/repositories-collector/) as follows:

```pip install repositories-collector```

Alternatively, it can be installed from the source code with:

```
pip install -r requirements.txt
pip install .
```

## Command-line usage

```
usage: repositories-collector [-h] [-v] [--from DATE_FROM]
                                    [--to DATE_TO] [--pushed-after DATE_PUSH]
                                    [--min-issues MIN_ISSUES]
                                    [--min-releases MIN_RELEASES]
                                    [--min-stars MIN_STARS]
                                    [--min-watchers MIN_WATCHERS] [--verbose]
                                    dest

A Python library to collect repositories metadata from GitHub.

positional arguments:
  dest                  destination folder for report

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --from DATE_FROM      collect repositories created since this date (default:
                        2014-01-01 00:00:00)
  --to DATE_TO          collect repositories created up to this date (default:
                        2014-01-01 00:00:00)
  --pushed-after DATE_PUSH
                        collect only repositories pushed after this date
                        (default: 2019-01-01 00:00:00)
  --min-issues MIN_ISSUES
                        collect repositories with at least <min-issues> issues
                        (default: 0)
  --min-releases MIN_RELEASES
                        collect repositories with at least <min-releases>
                        releases (default: 0)
  --min-stars MIN_STARS
                        collect repositories with at least <min-stars> stars
                        (default: 0)
  --min-watchers MIN_WATCHERS
                        collect repositories with at least <min-watchers>
                        watchers (default: 0)
  --verbose             show log (default: False)
```


**Important!** The tool requires a personal access token to access the GraphQL APIs. See how to get one [here](https://github.com/settings/tokens).
Add ```GITHUB_ACCESS_TOKEN=<paste here your token>``` to the environment variables.


### Output
Running the tool from command-line generates an HTML report accessible at *\<dest\>/report.html*.


## Contributions

To report bugs, visit the
[issue tracker](https://github.com/radon-h2020/radon-repositories-collector/issues).

In case you want to play with the source code or contribute improvements, see
[CONTRIBUTING](#).

## Version
**[0.0.2]** 
Fixed missed import of config.json in MANIFEST.in

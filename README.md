# radon-repositories-collector
A tool to query GraphQL for collecting repositories metadata.


## How to install

A PyPIP package will be available soon! 
In the meantime, install it from source code with:

```
pip install -r requirements.txt
pip install .
```

## Command-line usage

```
usage: radon-repositories-collector [-h] [-v] [--from DATE_FROM]
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
Once generated, paste the token in the input field when asked. For example:

```
radon-repositories-collector . --from 2020-01-01 --to 2020-01-02

Github access token: <paste your token here>
```  

You may want to avoid the previous step. If so, add ```GITHUB_ACCESS_TOKEN=<paste here your token>``` to the environment variables.


### Output
Running the tool from command-line generates an HTML report accessible at *\<dest\>/report.html*.
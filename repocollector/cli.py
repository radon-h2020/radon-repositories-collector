import argparse
import copy
import io
import json
import os

from datetime import datetime
from getpass import getpass

from repocollector.github import GithubRepositoriesCollector
from repocollector.report import create_report

VERSION = "0.0.3"


def date(x: str) -> datetime:
    """
    Check the passed date is well-formatted
    :param x: a datetime
    :return: datetime(x); raise an ArgumentTypeError otherwise
    """
    try:
        # String to datetime
        x = datetime.strptime(x, '%Y-%m-%d')
    except Exception:
        raise argparse.ArgumentTypeError('Date format must be: YYYY-MM-DD')

    return x


def unsigned_int(x: str) -> int:
    """
    Check the number is greater than or equal to zero
    :param x: a number
    :return: int(x); raise an ArgumentTypeError otherwise
    """
    x = int(x)
    if x < 0:
        raise argparse.ArgumentTypeError('Minimum bound is 0')
    return x


def valid_path(x: str) -> str:
    """
    Check the path exists
    :param x: a path
    :return: the path if exists; raise an ArgumentTypeError otherwise
    """
    if not os.path.isdir(x):
        raise argparse.ArgumentTypeError('Insert a valid path')

    return x


def get_parser():
    description = 'A Python library to collect repositories metadata from GitHub.'

    parser = argparse.ArgumentParser(prog='repositories-repocollector', description=description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)

    parser.add_argument(action='store',
                        dest='since',
                        type=date,
                        default=datetime.strptime('2014-01-01', '%Y-%m-%d'),
                        help='collect repositories created since this date (default: %(default)s)')

    parser.add_argument(action='store',
                        dest='until',
                        type=date,
                        default=datetime.strptime('2014-01-01', '%Y-%m-%d'),
                        help='collect repositories created up to this date (default: %(default)s)')

    parser.add_argument(action='store',
                        dest='dest',
                        type=valid_path,
                        help='destination folder for report')

    parser.add_argument('--pushed-after',
                        action='store',
                        dest='date_push',
                        type=date,
                        default=datetime.strptime('2019-01-01', '%Y-%m-%d'),
                        help='collect only repositories pushed after this date (default: %(default)s)')

    parser.add_argument('--min-issues',
                        action='store',
                        dest='min_issues',
                        type=unsigned_int,
                        default=0,
                        help='collect repositories with at least <min-issues> issues (default: %(default)s)')

    parser.add_argument('--min-releases',
                        action='store',
                        dest='min_releases',
                        type=unsigned_int,
                        default=0,
                        help='collect repositories with at least <min-releases> releases (default: %(default)s)')

    parser.add_argument('--min-stars',
                        action='store',
                        dest='min_stars',
                        type=unsigned_int,
                        default=0,
                        help='collect repositories with at least <min-stars> stars (default: %(default)s)')

    parser.add_argument('--min-watchers',
                        action='store',
                        dest='min_watchers',
                        type=unsigned_int,
                        default=0,
                        help='collect repositories with at least <min-watchers> watchers (default: %(default)s)')

    parser.add_argument('--primary-language',
                        action='store',
                        dest='primary_language',
                        type=str,
                        default=None,
                        help='collect repositories written in this language')

    parser.add_argument('--verbose',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='show log (default: %(default)s)')

    return parser


def main():
    args = get_parser().parse_args()

    token = os.getenv('GITHUB_ACCESS_TOKEN')
    if not token:
        token = getpass('Github access token:')

    github = GithubRepositoriesCollector(
        access_token=token,
        since=args.since,
        until=args.until,
        pushed_after=args.date_push,
        min_stars=args.min_stars,
        min_releases=args.min_releases,
        min_watchers=args.min_watchers,
        min_issues=args.min_issues,
        primary_language=args.primary_language
    )

    repositories = list()
    for repository in github.collect_repositories():

        # Save repository to collection
        repositories.append(copy.deepcopy(repository))

        if args.verbose:
            print(f'Collected {repository["url"]}')

    # Generate html report
    html = create_report(repositories)
    html_filename = os.path.join(args.dest, 'repositories.html')
    json_filename = os.path.join(args.dest, 'repositories.json')

    with io.open(html_filename, "w", encoding="utf-8") as f:
        f.write(html)

    with io.open(json_filename, "w") as f:
        json.dump(repositories, f)

    if args.verbose:
        print(f'Report created at {html_filename}')

    exit(0)

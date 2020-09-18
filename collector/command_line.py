import argparse
import copy
import io
import json
import os

from datetime import datetime
from dotenv import load_dotenv
from getpass import getpass

from collector.github import GithubRepositoriesCollector
from collector.report import create_report

with open('config.json', 'r') as in_stream:
    configuration = json.load(in_stream)

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

    parser = argparse.ArgumentParser(prog='repositories-collector', description=description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + configuration.get('version', '0.0'))

    parser.add_argument(action='store',
                        dest='dest',
                        type=valid_path,
                        help='destination folder for report')

    parser.add_argument('--from',
                        action='store',
                        dest='date_from',
                        type=date,
                        default=datetime.strptime('2014-01-01', '%Y-%m-%d'),
                        help='collect repositories created since this date (default: %(default)s)')

    parser.add_argument('--to',
                        action='store',
                        dest='date_to',
                        type=date,
                        default=datetime.strptime('2014-01-01', '%Y-%m-%d'),
                        help='collect repositories created up to this date (default: %(default)s)')

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

    parser.add_argument('--verbose',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='show log (default: %(default)s)')

    return parser



def main():
    args = get_parser().parse_args()

    load_dotenv()

    token = os.getenv('GITHUB_ACCESS_TOKEN')
    if not token:
        token = getpass('Github access token:')

    github = GithubRepositoriesCollector(
        access_token=token,
        date_from=args.date_from,
        date_to=args.date_to,
        pushed_after=args.date_push,
        min_stars=args.min_stars,
        min_releases=args.min_releases,
        min_watchers=args.min_watchers,
        min_issues=args.min_issues
    )

    repositories = list()
    for repository in github.collect_repositories():

        if args.verbose:
            print(f'Collecting {repository["url"]} ... ', end='', flush=True)

        # Save repository to collection
        repositories.append(copy.deepcopy(repository))

        if args.verbose:
            print('DONE')

    # Generate html report
    html = create_report(repositories)
    filename = os.path.join(args.dest, 'report.html')

    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    if args.verbose:
        print(f'Report created at {filename}')

    exit(0)

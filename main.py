import requests
import getpass

import pandas as pd
import argparse

from exceptions import *

BASE_URL = 'https://api.github.com'
COLUMNS_NAME = ['repo', 'amount of branches']
TOKEN = 'token'


class GitHubClient(object):
    """
    Manages the connection to GitHub API
    """

    def __init__(self, base_url: str, organization: str, username: str = None, password: str = None, token: str = None):
        self.__base_url = base_url
        self.__organization = organization
        self.__username = username
        self.__password = password
        self.__token = token
        self.github_client = requests.Session()

        if password and username is not None:
            self.github_client.auth = (username, password)
        elif not len(token) == 0:
            self.github_client.auth = (TOKEN, token)
        else:
            raise AuthenticationDetailsNotGiven

    def make_get_api_call(self, endpoint: str):
        """
        :param endpoint: The url endpoint to fetch
        :return: The data fetched from the api call
        """
        url = self.__base_url + endpoint
        request_data = self.github_client.get(url)
        if request_data.status_code != 200:
            raise HttpResponseError(request_data.status_code)
        return request_data.json()

    def get_repos_names(self):
        """
        :return: A list of all repos in a specific organization
        """
        endpoint = f"/orgs/{self.__organization}/repos"
        repos_raw_data = self.make_get_api_call(endpoint)
        return [repo['name'] for repo in repos_raw_data]

    def get_branches_names(self, repo: dict):
        """
        :param repo: A repo to search through
        :return: A list of all branches in a specific repo
        """
        endpoint = f'/repos/{self.__organization}/{repo}/branches'
        return [branch['name'] for branch in self.make_get_api_call(endpoint)]


def convert_dict_to_table(my_dict: dict, column_names: list):
    """
    :param my_dict: A dictionary we want to convert
    :param column_names: The tables column names
    :return: A table based on the info from the original dict
    """
    if bool(my_dict):
        table = pd.DataFrame(my_dict.items(), columns=column_names)
        return table
    return "No data found"


def branch_count_from_organization_repos():
    """
    Prints a Table with all repos and their branches in a specific organization
    """
    parser = argparse.ArgumentParser(description="GitHub organization branch count")
    parser.add_argument("--username", help="the username is", type=str)
    parser.add_argument("--organization", help="the organization name is", type=str)
    args = parser.parse_args()
    user_auth = getpass.getpass(prompt='Enter your token / password \n')

    github_client = GitHubClient(BASE_URL,
                                 organization=args.organization,
                                 username=args.username,
                                 password=user_auth,
                                 token=user_auth)

    repos = github_client.get_repos_names()
    repos_branched_counter = {repo: len(github_client.get_branches_names(repo)) for repo in repos}
    print(convert_dict_to_table(repos_branched_counter, column_names=COLUMNS_NAME))


if __name__ == '__main__':
    branch_count_from_organization_repos()

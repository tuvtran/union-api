from fabric.contrib.files import exists
from fabric.context_managers import shell_env
from fabric.api import env, local, run

REPO_URL = 'https://github.com/tuvttran/union-api.git'


def deploy(sitename: str, db_info: str, app_settings: str="staging") -> None:
    site_folder: str = f'/home/{env.user}/sites/{sitename}'
    source_folder: str = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder, app_settings)
    _update_virtualenv(source_folder)
    _update_database(source_folder, db_info, app_settings)


def _create_directory_structure_if_necessary(site_folder: str) -> None:
    for subfolder in ('virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder: str, app_settings: str):
    branchname: str = "master" if app_settings == "production" else "staging"
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch origin {branchname}')
    else:
        run(f'git clone -b {branchname} {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_virtualenv(source_folder: str):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -U setuptools')
    run(f'{virtualenv_folder}/bin/pip install -r \
        {source_folder}/requirements.txt')


def _update_database(
        source_folder: str, db_info: str, app_settings: str):
    with shell_env(
        DATABASE_URL='postgresql://' + db_info,
        APP_SETTINGS=app_settings
    ):
        run(
            f'cd {source_folder}'
            ' && ../virtualenv/bin/python manage.py db upgrade'
        )
        run(
            f'cd {source_folder}'
            ' && ../virtualenv/bin/python manage.py populate'
        )

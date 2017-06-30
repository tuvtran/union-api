from fabric.contrib.files import exists
from fabric.context_managers import shell_env
from fabric.api import env, local, run

REPO_URL = 'https://github.com/tuvttran/union-api.git'


def deploy(sitename, db_info):
    site_folder = f'/home/{env.user}/sites/{sitename}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_virtualenv(source_folder)
    _update_database(source_folder, db_info)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r \
        {source_folder}/requirements.txt')


def _update_database(source_folder, db_info):
    with shell_env(
        DATABASE_URL='postgresql://' + db_info,
        APP_SETTINGS="staging"
    ):
        run(
            f'cd {source_folder}'
            ' && ../virtualenv/bin/python manage.py db upgrade'
        )

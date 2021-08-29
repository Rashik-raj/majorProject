# RecoznizeMe
Final year major project to identify nepali lipi

# how to run
1. Clone the project and change the dir to the project.
2. Run `git lfs pull master`.
3. Create virtual env by `python -m venv env` next to **manage.py** file.
4. Activate virtual env by `source env/bin/activate`.
5. Install requirements from requirements.txt file by `pip install -r requirements.txt`.
6. Create migration files `python manage.py makemigrations`.
7. Migrate database `python manage.py migrate`.
8. Run the server by `python manage.py runserver`.

# deploy on heroku
1. `heroku create rashik-major-project --buildpack heroku/python`
2. `heroku buildpacks:add https://github.com/raxod502/heroku-buildpack-git-lfs -a rashik-major-project`
3. `heroku config:set HEROKU_BUILDPACK_GIT_LFS_REPO=https://github.com/Rashik-raj/majorProject.git`
4. `git push heroku master --no-verify`

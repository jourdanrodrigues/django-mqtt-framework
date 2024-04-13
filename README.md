# dj_mqtt

_Generated from [Jourdan's Django template](https://github.com/jourdanrodrigues/django-template)._

This project runs entirely on Docker containers. Make sure to [have it](https://www.docker.com/community-edition#/download) in your environment.

## Linter

This projects makes use of [`pre-commit`](https://pre-commit.com/#install). Make sure it's installed in your dev-environment with the following command:

```bash
pre-commit install
```

## Database

This project depends on PostgreSQL and the connection is established through an environment variable called
DATABASE_URL. Check the files [.env.example](.env.example) and [docker-compose.yml](docker-compose.yml) for details.

## Running the app

The script [`compose.sh`](compose.sh) is there for you to run commands in the container. It's a simple wrapper around
 `docker-compose`, so you might want to take a look at [its documentation](https://docs.docker.com/compose/reference/).

```bash
./compose.sh up
```

### `./compose.sh` shortcuts

The script has the same API as docker-compose, with a few adjustments:

```bash
# Running development setup
./compose.sh dev up  # becomes the below
docker compose -f docker compose.yml -f docker compose.dev.yml up

# "run"
./compose.sh run server sh  # becomes the below
docker compose run --rm server sh

# "manage.py" commands
./compose.sh run manage.py test  # becomes the below
docker compose run --rm server python manage.py test
```

- `~ dev ~` = `~ -f docker compose.yml -f docker compose.dev.yml ~`
- `~ run ~` = `~ run --rm ~`
- `~ manage.py ~` = `~ server manage.py ~`

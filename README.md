File .env will be added to the repository for convenience
In real project I wouldn't do that

To run project type:
docker-compose up -d

Api docs will be in url:
http://localhost:8000/docs

To run project locally
First run migrations with typing:
alembic upgrade head (Configure postgresql before it)
and then type:
python3 main.py

I would put all these files to folders, but for convenience I didn't do that
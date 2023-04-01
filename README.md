# hackathon-music-recommender

Music recommender backend

To run the API you need to follow these steps:

1. Run `python3 -m venv .venv` to create a virtual environment
2. Run `source ./.venv/bin/activate` to activate the environment
3. Run `python3 -m pip install -r requirements.txt`
4. Copy the `dist.env` into a new `.env` file
5. Create a spotify developer project with the following redirect URL: `http://localhost:8080/callback`
6. Copy the credentials into the `.env` file
7. Create an OpenAI account and copy the API key into the .env file
8. Login with spotify following the steps when you run `python3 login.py` (Only need to run this script the first time)
9. If the login is successful you will be able to run `docker-compose up -d --build`
10. You can make a `POST` request to `http://localhost:8080/recomend` when the container is running to get the recomendations. The format of the request body follows the `RequestModel` defined in `src/models/base.py`

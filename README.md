# RihnoBot
A Telegram autofilter bot with file indexing and user credits.

## Features
- Random reactions on `/start`.
- Autofilter files from MongoDB.
- Admin file indexing with `/index`.
- User credits system.

## Setup
1. Clone the repo: `git clone https://github.com/yourusername/RihnoBot.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your values.
4. Run: `python main.py`

## Deployment
- **Docker**: `docker build -t rihnobot . && docker run -d rihnobot`
- **Heroku**: Push to Heroku with `Procfile` and `app.json`.
- **Render**: Use `render.yaml`.
- **Okteto**: Use `okteto-compose.yml`.

## License
MIT
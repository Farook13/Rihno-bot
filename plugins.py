# plugins/web_server.py
from aiohttp import web

async def web_server():
    async def hello(request):
        return web.Response(text="Telegram Movie Bot is running!")
    
    app = web.Application()
    app.router.add_get('/', hello)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)  # Port 8000 hardcoded
    await site.start()
    return runner
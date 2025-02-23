from aiohttp import web

async def web_server():
 async def hello(request):
 return web.Response(text="Telegram Movie Bot is running!")
 app = web.Application()
 app.router.add_get('/', hello)
 return app

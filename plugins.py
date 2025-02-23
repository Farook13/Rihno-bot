from aiohttp import web

async def web_server():
    async def hello(request):
        return web.Response(text="Telegram Movie Bot is running!")
    
    app = web.Application()
    app.router.add_get('/', hello)
    return app

# To actually run the server, you would typically add:
# if __name__ == '__main__':
#     web.run_app(web_server())
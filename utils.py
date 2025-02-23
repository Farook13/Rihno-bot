# utils.py
from config import LOGGER

def get_file_size(file):
    size = file.file_size
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

# Hypothetical web function
async def start_web():
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)  # Port 8000 hardcoded
    await site.start()
    return runner
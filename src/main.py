import time

from fastapi import FastAPI
from starlette.requests import Request

from src.suppliers.views import supplier_route


app = FastAPI()
app.include_router(
	supplier_route,
	prefix='/supplier',
	tags=['Suppliers']
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event('startup')
async def load_configs():
	from src.config import load_config_file
	load_config_file()


@app.on_event('shutdown')
async def clear_config_caches():
	from src.config import load_config_file, read_config_file, get_config
	get_config.cache_clear()
	load_config_file.cache_clear()
	read_config_file.cache_clear()
from fastapi import FastAPI
from app.db.register import init_db
from app.core.views import ItemAPI, ClockInAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    
    items_collection, clock_in_collection = await init_db(app)
    
    # Initialize your ItemAPI class with the collections
    item_api = ItemAPI(items_collection)
    clock_in_api = ClockInAPI(clock_in_collection)
    
    # Include the router from ItemAPI
    app.include_router(item_api.get_router())  # Call get_router() to include it
    app.include_router(clock_in_api.get_router())

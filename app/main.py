from fastapi import FastAPI
from app.db.register import init_db
from app.core.views import ItemAPI, ClockInAPI

app = FastAPI(
    title="Vodex AI",
    description="Vodex AI Assignment",
    version="1.0.0",
    docs_url="/docs",  # Default is /docs
    redoc_url="/redoc"  # Default is /redoc
)

@app.on_event("startup")
async def startup_event():
    
    items_collection, clock_in_collection = await init_db(app)
    
    # Initialize your ItemAPI class with the collections
    item_api = ItemAPI(items_collection)
    clock_in_api = ClockInAPI(clock_in_collection)
    
    # Include the router from ItemAPI
    app.include_router(item_api.get_router())  # Call get_router() to include it
    app.include_router(clock_in_api.get_router())

# Sample /hello GET endpoint
@app.get("/hello")
async def hello():
    return {"message": "Hello, Welcome to Vodex AI!"}
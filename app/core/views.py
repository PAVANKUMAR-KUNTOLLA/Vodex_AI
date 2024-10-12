from fastapi import FastAPI, HTTPException, APIRouter, Depends, Query
from typing import List, Optional
from datetime import date, datetime
from .schema import ItemCreate, ItemResponse, ItemUpdate, ItemFilterRequest, ItemAggregationResponse, ClockInCreate, ClockInUpdate, ClockInResponse, ClockInFilterRequest

class ItemAPI:
    def __init__(self, items_collection):
        self.items_collection = items_collection
        self.items_router = APIRouter()

        # Registering the routes
        self.items_router.add_api_route("/items", self.create_item, methods=["POST"], response_model=ItemResponse)
        self.items_router.add_api_route("/items/filter", self.filter_items, methods=["GET"], response_model=List[ItemResponse])
        self.items_router.add_api_route("/items/aggregate", self.aggregate_items, methods=["GET"], response_model=List[ItemAggregationResponse])
        self.items_router.add_api_route("/items/{item_id}", self.get_item, methods=["GET"], response_model=ItemResponse)
        self.items_router.add_api_route("/items/{item_id}", self.update_item, methods=["PUT"], response_model=ItemResponse)
        self.items_router.add_api_route("/items/{item_id}", self.delete_item, methods=["DELETE"], response_model=dict)

    async def create_item(self, item: ItemCreate):
        insert_date = datetime.now().strftime('%Y-%m-%d')
        item_data = item.dict()
        item_data["insert_date"] = insert_date
        item_data["item_id"] = item._item_id
        item_data["expiry_date"] = item._expiry_date
        await self.items_collection.insert_one(item_data)
        return self.item_to_response(item_data)

    async def get_item(self, item_id: str):
        item = await self.items_collection.find_one({"item_id": item_id})
        if item:
            return self.item_to_response(item)
        raise HTTPException(status_code=404, detail="Item not found")

    async def filter_items(self, filters: ItemFilterRequest = Depends()):
        query = {}
        print("filters:", filters)
        
        if filters.email:
            query["email"] = filters.email
        if filters.expiry_date_after:
            query["expiry_date"] = {"$gt": filters.expiry_date_after}
        if filters.insert_date_after:
            query["insert_date"] = {"$gt": filters.insert_date_after}
        if filters.quantity_gte is not None:
            query["quantity"] = {"$gte": filters.quantity_gte}

        # Convert cursor to a list with to_list()
        items = await self.items_collection.find(query).to_list(length=None)

        return [self.item_to_response(item) for item in items]


    async def delete_item(self, item_id: str):
        result = await self.items_collection.delete_one({"item_id": item_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}

    async def update_item(self, item_id: str, item_update: ItemUpdate):
        # Create a dictionary of non-None values for update
        update_data = {k: v for k, v in item_update.dict().items() if v is not None}

        # Debug print statements
        print("item_update:", item_update)
        print("update_data:", update_data)

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields provided for update")

        # Perform the update operation
        result = await self.items_collection.update_one({"item_id": item_id}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Item not found or no changes made")

        # Retrieve and return the updated item
        updated_item = await self.items_collection.find_one({"item_id": item_id})
        return self.item_to_response(updated_item)

    async def aggregate_items(self) -> List[ItemAggregationResponse]:
        pipeline = [
            {"$group": {"_id": "$email", "count": {"$sum": 1}}},
            {"$project": {"email": "$_id", "count": 1, "_id": 0}}
        ]
        # Use async iteration or to_list() to handle the cursor
        cursor =  self.items_collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)  # Collect all results from the cursor

        # Process the results into response format
        return [ItemAggregationResponse(email=item["email"], count=item["count"]) for item in result]
    
    def item_to_response(self, item_data):
        return ItemResponse(
            item_id=item_data["item_id"],
            name=item_data["name"],
            email=item_data["email"],
            item_name=item_data["item_name"],
            quantity=item_data["quantity"],
            expiry_date=item_data.get('expiry_date').strftime('%Y-%m-%d') if isinstance(item_data.get('expiry_date'), datetime) else item_data.get('expiry_date'),
            insert_date=item_data.get('insert_date').strftime('%Y-%m-%d') if isinstance(item_data.get('insert_date'), datetime) else item_data.get('insert_date')
        )

    def get_router(self):
        return self.items_router


class ClockInAPI:
    def __init__(self, clock_in_collection):
        self.clock_in_collection = clock_in_collection
        self.clock_in_router = APIRouter()

        # Registering the routes
        self.clock_in_router.add_api_route("/clock-in", self.create_clock_in, methods=["POST"], response_model=ClockInResponse)
        self.clock_in_router.add_api_route("/clock-in/filter", self.filter_clock_in, methods=["GET"], response_model=List[ClockInResponse])
        self.clock_in_router.add_api_route("/clock-in/{clock_in_id}", self.get_clock_in, methods=["GET"], response_model=ClockInResponse)
        self.clock_in_router.add_api_route("/clock-in/{clock_in_id}", self.update_clock_in, methods=["PUT"], response_model=ClockInResponse)
        self.clock_in_router.add_api_route("/clock-in/{clock_in_id}", self.delete_clock_in, methods=["DELETE"], response_model=dict)

    async def create_clock_in(self, clock_in: ClockInCreate):
        insert_datetime = datetime.now().strftime('%Y-%m-%d')
        clock_in_data = clock_in.dict()
        clock_in_data["insert_datetime"] = insert_datetime
        clock_in_data["clock_in_id"] = clock_in._clock_in_id
        await self.clock_in_collection.insert_one(clock_in_data)
        return self.clock_in_to_response(clock_in_data)

    async def get_clock_in(self, clock_in_id: str):
        clock_in = await self.clock_in_collection.find_one({"clock_in_id": clock_in_id})
        if clock_in:
            return self.clock_in_to_response(clock_in)
        raise HTTPException(status_code=404, detail="Clock-In record not found")

    async def filter_clock_in(self, filters: ClockInFilterRequest = Depends()):
        query = {}
        if filters.email:
            query["email"] = filters.email
        if filters.location:
            query["location"] = filters.location
        if filters.insert_datetime_after:
            query["insert_datetime"] = {"$gt": filters.insert_datetime_after.isoformat()}

        # Convert cursor to a list with to_list()
        clock_ins = await self.clock_in_collection.find(query).to_list(length=None)

        return [self.clock_in_to_response(clock_in) for clock_in in clock_ins]

    async def delete_clock_in(self, clock_in_id: str):
        result = await self.clock_in_collection.delete_one({"clock_in_id": clock_in_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Clock-In record not found")
        return {"message": "Clock-In record deleted successfully"}

    async def update_clock_in(self, clock_in_id: str, clock_in_update: ClockInUpdate):
        # Create a dictionary of non-None values for update
        update_data = {k: v for k, v in clock_in_update.dict().items() if v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields provided for update")

        result = await self.clock_in_collection.update_one({"clock_in_id": clock_in_id}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Clock-In record not found or no changes made")

        updated_clock_in = await self.clock_in_collection.find_one({"clock_in_id": clock_in_id})
        return self.clock_in_to_response(updated_clock_in)

    def clock_in_to_response(self, clock_in_data):
        return ClockInResponse(
            clock_in_id=clock_in_data["clock_in_id"],
            email=clock_in_data["email"],
            location=clock_in_data["location"],
            insert_datetime=clock_in_data.get('insert_datetime')
        )

    def get_router(self):
        return self.clock_in_router

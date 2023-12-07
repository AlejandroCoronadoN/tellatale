"""Main Entrypoint."""
import math

import agents.api.schemas
import pandas as pd
from config.configuration import SETTINGS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

BRANCH_ID = "MSC-10001"
df_users = pd.read_csv("users.csv")
df_entries = pd.read_csv("entries.csv")

ORDERS = {}

app = FastAPI(
    title="Tell a tale",
    description="LLM diary that displays beautiful images after loading personal diary data",
    version=SETTINGS.version,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
app.mount("/assets", StaticFiles(directory="../frontend/build/assets"), name="static")


def update_orders(product_id: str, qty: int):
    """Adds or deletes products from the customer cart depending on the action performed by the user. If a product is scanned the we increase the quantity order. If the product is deleted then we decrease the quantity order.

    Raises:
        product_id: Number of the product
        ValueError:

    Returns:
        dict: _description_
    """
    product_id = int(product_id)
    if product_id in ORDERS.keys():
        ORDERS[product_id] += qty
    else:
        ORDERS[product_id] = qty
    if ORDERS[product_id] < 0:
        raise ValueError(
            "You are trying to delete more items than the ones you have in your cart"
        )


def calculate_taxes(branch_id: str) -> int:
    """Calculates taxtes depending on the branch.

    Args:
        branch_id (str): _description_

    Returns:
        int: _description_
    """
    return 8.25


def create_product_message(product_id: dict, cmp: bool = False) -> dict:
    """Creates a formatted response with the details of the products associated with the products id.

    Raises:
        product_id: Number of the product
        ValueError:

    Returns:
        dict: _description_
    """
    df_product_info = df_products[df_products.ProductID == product_id]

    if len(df_product_info) > 1:
        raise ValueError("There is more than product associated with that id ")
    elif len(df_product_info) == 0:
        raise ValueError(
            "There are no products on the database associated with that product_id"
        )
    if not cmp:
        order = ORDERS[product_id]
    else:
        order = 0
    response = {
        "model": df_product_info["Model #"].item(),
        "description": df_product_info["ProductDescriptionLine1and2"].item(),
        "mfg": df_product_info["MFG"].item(),
        "stock": df_product_info["Start Up Stock Qty"].item(),
        "area": df_product_info["Area"].item(),
        "recommendation": df_product_info["RECOMMENDATIONPRODUCTID"].item(),
        "cmp_price": df_product_info["COMPETITIVEMARKETPRICE"].item(),
        "user_price": df_product_info["TRADEPRICE"].item(),
        "image_url": df_product_info["Image URL"].item(),
        "order": order,
        "taxes": calculate_taxes(BRANCH_ID),
    }
    return response


@app.get("/")
async def read_index() -> HTMLResponse:
    """This function reads the contents of the index.html file and returns it as an HTMLResponse.

    :return: The contents of the index.html file as an HTMLResponse.
    :rtype: HTMLResponse
    """
    with open("../frontend/build/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/scan_user")
def get_user_information(user_id: agents.api.schemas.UserMessage):
    """Creates a stream of responses from the AI agent for the given prompt.

    Args:
        message (str): messaged prompt for AI agent
    Yields:
        Iterator[AsyncIterable[str]]: yields a stream of responses from the AI agent
    """
    df_selected_user = df_users[df_users.user_id == int(user_id.message)]
    if len(df_selected_user) == 0:
        raise ValueError("No users where detected with the passed id ")
    result = {
        "name": df_selected_user.First.item() + " " + df_selected_user.Last.item(),
        "user_id": df_selected_user.user_id.item(),
    }
    return result



@app.get("/ping")
async def ping():
    """A function that returns a dictionary with a message key and a value of "pong 🏓"."""
    logger.info("Ping received")
    return {"message": "pong 🏓"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# Copyright 2022-2023 iiPython

# Modules
import os
import json
import time
from blacksheep import Request
from blacksheep.server.responses import not_found

from . import app, root, view

# Configuration
season_folder = os.path.join(root, "garchive/static/seasons")

# Routes
@app.route("/")
async def route_home() -> None:
    return await view("home", {})

@app.route("/seasons")
async def route_seasons() -> None:
    seasons = []
    for s in os.listdir(season_folder):
        with open(os.path.join(season_folder, s, "season.json"), "r") as fh:
            data = json.loads(fh.read())

        data["id"] = s
        seasons.append(data)

    return await view(
        "seasons",
        {
            "seasons": sorted(seasons, key = lambda s: s["timestamp"] or time.time() * 1000, reverse = True)
        }
    )

@app.route("/seasons/{sid}")
async def route_details(request: Request, sid: str) -> None:
    season_path = os.path.join(season_folder, sid)
    season_json = os.path.join(season_path, "season.json")
    if not os.path.isfile(season_json):
        return not_found("No such season exists.")

    # Load season information
    with open(season_json, "r") as fh:
        data = json.loads(fh.read())
        data["id"] = sid
        data["download"] = os.path.isfile(os.path.join(season_path, "download.zip"))
        data["gallery"] = [x for x in os.listdir(os.path.join(season_path, "gallery")) if x.endswith(".png")]

    # Render template
    return await view(
        "details.html",
        {
            "data": data
        }
    )

@app.route("/")
async def route_status() -> None:
    return await view("status", {})

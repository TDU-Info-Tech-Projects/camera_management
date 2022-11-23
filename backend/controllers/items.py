from crypt import methods
from datetime import datetime, timedelta
from http.client import OK, UNPROCESSABLE_ENTITY, UNAUTHORIZED
from time import timezone
from flask import jsonify, request, abort, Response
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from os import urandom
from database import engine
from controllers.main import bp
from database.models import Item, Mount, RentItem
from services import validate_email, validate_password
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from services.middleware import validate_fullname, protected
import jwt
import os


@bp.route("/mounts/add", methods=('POST',))
@protected(admin_only=True)
def register_mount():
    mount = None
    req = request.json
    if "id" in req:
        with Session(engine) as session:
            mount = session.query(Mount).where(Mount.id == req["id"]).one()
    if mount is None:
        mount = Mount()

    mount.name = req["name"]

    with Session(engine) as session, session.begin():
        session.merge(mount)

    return Response(status=OK)


@bp.route("/mounts/delete", methods=('POST',))
@protected(admin_only=True)
def unregister_mount():
    req = request.json
    with Session(engine) as session, session.begin():
        mount = session.query(Mount).where(Mount.id == req["id"]).one()
        session.delete(mount)
        session.commit()
    return Response(status=OK)


@bp.route("/mounts")
def get_mounts():
    with Session(engine) as session:
        result = session.execute(select(Mount))
        mounts = result.scalars().all()
        return jsonify(mounts)


@bp.route("/items/add", methods=('POST',))
@protected(admin_only=True)
def register_item():
    item = None
    req = request.json
    if "id" in req:
        with Session(engine) as session:
            item = session.query(Item).where(Item.id == req["id"]).one()
    if item is None:
        item = Item()

    item.name = req["name"]
    item.image_url = req["image_url"]
    item.stock = req["stock"]
    item.is_consumable = req["is_consumable"]
    item.is_lens = req["is_lens"]
    item.description = req["description"]
    # item.category_id = req["category_id"]
    # item.manufacture_id = req["manufacture_id"]
    item.mount_id = req["mount_id"]
    item.release = req["release"]

    with Session(engine) as session, session.begin():
        session.merge(item)

    return Response(OK)


@bp.route("/items/delete", methods=('POST',))
@protected(admin_only=True)
def unregister_item():
    req = request.json
    with Session(engine) as session, session.begin():
        # stmt = delete(RentItem).where(RentItem.item_id == req["id"])
        # session.execute(stmt)
        # TODO: check if auto cascade delete works
        item = session.query(Item).where(Item.id == req["id"]).one()
        session.delete(item)
    return Response(status=OK)


@bp.route("/items")
def get_items():
    with Session(engine) as session:
        result = session.execute(select(Item))
        items = result.scalars().all()
        return jsonify(items)

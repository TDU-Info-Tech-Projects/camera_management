from http.client import OK
from flask import jsonify, request, Response
from database import engine
from controllers.main import bp
from database.models import Item, Mount
from sqlalchemy.orm import Session
from sqlalchemy import select
from services.middleware import protected


@bp.route("/mounts/add", methods=('POST',))
@protected(admin_only=True)
def register_mount():
    mount = None
    req = request.json
    if "id" in req and req["id"] != "":
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
    if "id" in req and req["id"] != "":
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
    item.mount_id = req["mount_id"]
    item.release = req["release"] if req["release"] else None

    with Session(engine) as session, session.begin():
        session.merge(item)

        return Response(status=OK)


@bp.route("/items/delete", methods=('POST',))
@protected(admin_only=True)
def unregister_item():
    req = request.json
    with Session(engine) as session, session.begin():
        item = session.query(Item).where(Item.id == req["id"]).one()
        session.delete(item)
        return Response(status=OK)


@bp.route("/items")
def get_items():
    with Session(engine) as session:
        result = session.execute(select(Item).order_by(Item.id))
        items = result.scalars().all()
        return jsonify(items)

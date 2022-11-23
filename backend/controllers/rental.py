from datetime import datetime
from datetime import datetime
from http.client import OK, UNPROCESSABLE_ENTITY

from flask import jsonify, request, abort, Response
from sqlalchemy import select, null
from sqlalchemy.orm import Session, join

from controllers.main import bp
from database import engine
from database.models import Item, RentItem, User
from services.middleware import protected


@bp.route("/items/rent", methods=("POST",))
@protected()
def rent_item():
    req = request.json
    print(req, flush=True)
    if "ids" not in req:
        abort(UNPROCESSABLE_ENTITY)

    # YYYY-MM-DD
    loan_date = datetime.now().date()
    due_date = None
    if req["due_date"] is not None:
        due_date = datetime.fromisoformat(req["due_date"]).date()

    if due_date is not None and due_date <= loan_date:
        abort(UNPROCESSABLE_ENTITY)

    user_email = request.user["email_address"]

    with Session(engine) as session, session.begin():
        user = session.execute(select(User).where(User.email_address == user_email)).scalar_one()
        items = session.execute(select(Item).where(Item.id.in_(req["ids"]))).scalars().all()
        rent_items = []
        for item in items:
            if item.stock < 1:
                abort(UNPROCESSABLE_ENTITY)

            return_date = None
            if not item.is_consumable and due_date is None:
                abort(UNPROCESSABLE_ENTITY)
            elif item.is_consumable:            
                due_date = datetime.now().date()
                return_date = datetime.now().date()

            rent_items.append(RentItem(
                user_id=user.id,
                item_id=item.id,
                loan_date=loan_date,
                due_date=due_date,
                return_date=return_date
            ))

            item.stock -= 1

        session.bulk_save_objects(items)
        session.add_all(rent_items)

    return Response(OK)


@bp.route("/items/rented")
@protected()
def rented_items():
    email = request.user["email_address"]
    with Session(engine) as session:
        user = session.execute(select(User).where(User.email_address == email)).scalar_one()
        all_items = {
            'returned_items': [],
            'due_items': []
        }

        queryRes = session.query(RentItem, Item).\
            join(Item).filter(RentItem.user_id == user.id).\
            filter(RentItem.return_date == None).\
            order_by(RentItem.due_date.desc()).\
            all()
        for res in queryRes:
            all_items['due_items'].append(res._asdict())

        queryRes = session.query(RentItem, Item).\
            join(Item).filter(RentItem.user_id == user.id).\
            filter(RentItem.return_date != None).\
            order_by(RentItem.due_date.desc()).\
            all()
        for res in queryRes:
            all_items['returned_items'].append(res._asdict())

        return jsonify(all_items)


@bp.route("/items/admin/rented")
@protected(admin_only=True)
def admin_rented_items():
    with Session(engine) as session:
        all_items = {
            'returned_items': [],
            'due_items': []
        }

        queryRes = session.query(RentItem, Item).\
            join(Item).filter(RentItem.return_date == None).\
            order_by(RentItem.due_date.desc()).\
            all()

        for res in queryRes:
            all_items['due_items'].append(res._asdict())

        queryRes = session.query(RentItem, Item).\
            join(Item).filter(RentItem.return_date != None).\
            order_by(RentItem.due_date.desc()).\
            all()
        for res in queryRes:
            all_items['returned_items'].append(res._asdict())

        return jsonify(all_items)


@bp.route("/items/overdue")
@protected()
def overdue_items():
    email = request.user["email_address"]
    with Session(engine) as session, session.begin():
        user = session.execute(select(User).where(User.email_address == email)).scalar_one()

        queryRes = session.query(RentItem, Item).\
            join(Item).filter(RentItem.return_date == None).\
            filter(RentItem.due_date < datetime.now().date()).\
            filter(RentItem.user_id == user.id).\
            order_by(RentItem.due_date.desc()).\
            all()
            
        overdue_items = []
        for res in queryRes:
            overdue_items.append(res._asdict())

        return jsonify(overdue_items)

@bp.route("/items/admin/overdue")
@protected()
def admin_overdue_items(admin_only=True):
    with Session(engine) as session, session.begin():

        queryRes = session.query(RentItem, Item).\
            join(Item).filter(RentItem.return_date == None).\
            filter(RentItem.due_date < datetime.now().date()).\
            order_by(RentItem.due_date.desc()).\
            all()
            
        overdue_items = []
        for res in queryRes:
            overdue_items.append(res._asdict())

        return jsonify(overdue_items)


@bp.route("/items/return", methods=("POST",))
@protected()
def return_items():
    req = request.json
    if "ids" not in req:
        abort(UNPROCESSABLE_ENTITY)

    # YYYY-MM-DD
    return_date = datetime.now().date()

    user_email = request.user["email_address"]

    with Session(engine) as session, session.begin():
        user = session.execute(select(User).where(User.email_address == user_email)).scalar_one()
        rentItems = session.execute(select(RentItem).where(RentItem.id.in_(req["ids"]))).scalars().all()
        items = []

        for rentItem in rentItems:
            if rentItem.return_date or (rentItem.user_id != user.id and not request.user["is_admin"]):
                abort(UNPROCESSABLE_ENTITY)
            rentItem.return_date = return_date
            item = session.execute(select(Item).where(Item.id == rentItem.item_id)).scalar_one()
            item.stock += 1
            items.append(item)

        session.bulk_save_objects(rentItems)
        session.bulk_save_objects(items)

    return Response(OK)
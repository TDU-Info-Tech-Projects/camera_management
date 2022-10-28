from datetime import datetime
from datetime import datetime
from http.client import OK, UNPROCESSABLE_ENTITY

from flask import jsonify, request, abort, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from controllers.main import bp
from database import engine
from database.models import Item, RentItem, User
from services.middleware import protected


@bp.route("/items/rent", methods=("POST",))
@protected()
def rent_item():
    req = request.json
    if "ids" not in req:
        abort(UNPROCESSABLE_ENTITY)

    # YYYY-MM-DD
    loan_date = datetime.now().date()
    due_date = datetime.fromisoformat(req["due_date"]).date()

    if due_date <= loan_date:
        abort(UNPROCESSABLE_ENTITY)

    user_email = request.user["email_address"]

    with Session(engine) as session, session.begin():
        user = session.execute(select(User).where(User.email_address == user_email)).scalar_one()
        items = session.execute(select(Item).where(Item.id.in_(req["ids"]))).scalars().all()
        rent_items = []
        for item in items:
            if item.stock < 1:
                abort(UNPROCESSABLE_ENTITY)

            rent_items.append(RentItem(
                user_id=user.id,
                item_id=item.id,
                loan_date=loan_date,
                due_date=due_date
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
        # TODO: Join
        user = session.execute(select(User).where(User.email_address == email)).scalar_one()
        items = session.execute(select(RentItem).where(RentItem.user_id == user.id)).scalars().all()

        return jsonify(items)


import restful
from exts import db
from models import Menu


def menus(page, per_page):
    pagination = db.session.query(Menu).paginate(page=page, per_page=per_page)

    return restful.success({
        "items": [
            item.to_dict()
            for item in pagination.items
        ],
        "total": pagination.total,
    })

import restful
from exts import db
from models import Ability, Menu


def abilities(permission, page, per_page):
    query = db.session.query(Ability)
    if permission:
        query = query.filter(Ability.name.ilike(f"%{permission}%"))

    pagination = query.paginate(page=page, per_page=per_page)

    return restful.success({
        "items": [
            item.to_dict()
            for item in pagination.items
        ],
        "pn": page,
        "size": per_page,
        "total": pagination.total,
    })


def find_by_id(id_):
    ability = db.session.query(Ability).filter_by(id_=id_).one_or_none()
    if ability:
        ability = ability.to_dict()

    return restful.success(ability)


def delete_by_id(id_):
    ability = db.session.query(Ability).filter_by(id_=id_).one_or_none()
    if ability:
        db.session.delete(ability)
        db.session.commit()

    return restful.success({"id": id_})


def create(name, menu_ids):
    ability = db.session.query(Ability).filter_by(name=name).one_or_none()
    if ability:
        return restful.error("ability name exists")

    ability = Ability(name=name)
    ability.menus = db.session.query(Menu).filter(Menu.id_.in_(menu_ids)).all()
    db.session.add(ability)
    db.session.commit()
    return restful.success(ability.to_dict())


def update(id_, name, menu_ids):
    ability = db.session.query(Ability).filter_by(id_=id_).one_or_none()
    if not ability:
        return restful.error("ability not found")

    if name != ability.name:
        if db.session.query(Ability).filter_by(name=name).one_or_none():
            return restful.error("ability name exists")

        ability.name = name

    ability.menus = db.session.query(Menu).filter(Menu.id_.in_(menu_ids)).all()
    db.session.add(ability)
    db.session.commit()
    return restful.success(ability.to_dict())

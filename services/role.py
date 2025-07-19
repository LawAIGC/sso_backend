import restful
from exts import db
from models import Role, Menu, Ability


def roles(name, page, per_page):
    query = db.session.query(Role)
    if name:
        query = db.session.query(Role).filter(Role.name.ilike(f"%{name}%"))
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
    role = db.session.query(Role).filter_by(id_=id_).one_or_none()
    if role:
        role_dict = role.to_dict()
        role_dict["permission_ids"] = [menu.id_ for menu in role.get_menus()]
    else:
        role_dict = None

    return restful.success(role_dict)


def delete_by_id(id_):
    role = db.session.query(Role).filter_by(id_=id_).one_or_none()
    if role:
        db.session.delete(role)
        db.session.commit()

    return restful.success({"id": id_})


def create(permission_ids, role_name,  description):
    abilities = db.session.query(Ability).filter(Ability.id_.in_(permission_ids)).all()
    role = db.session.query(Role).filter_by(name=role_name).one_or_none()
    if role:
        return restful.error("role name exists")

    role = Role(name=role_name, display_name=role_name, description=description, abilities=abilities)  # noqa
    db.session.add(role)
    db.session.commit()
    return restful.success(role.to_dict())


def update(role_id, permission_ids, role_name,  description):
    role = db.session.query(Role).filter_by(id_=role_id).one_or_none()
    if not role:
        return restful.error("not found role")

    role.name = role_name
    role.description = description

    abilities = db.session.query(Ability).filter(Ability.id_.in_(permission_ids)).all()
    role.abilities = abilities
    db.session.add(role)
    db.session.commit()
    return restful.success(role.to_dict())

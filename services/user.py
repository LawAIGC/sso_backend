from datetime import datetime

from flask_jwt_extended import create_access_token

import restful
from exts import db
from models import User, Role


def login(username, password):
    user = db.session.query(User).filter_by(name=username).one_or_none()
    if not user:
        return restful.error("用户名或密码错误")

    if not user.validate_password(password):
        return restful.error("用户名或密码错误")

    user.last_login_at = datetime.now()
    user_roles = [
        {
            "id": role.id_,
            "name": role.name,
            "display_name": role.display_name,
            "description": role.description,
            "status": role.status,
        }
        for role in user.roles
    ]
    user_dict = user.to_dict()
    user_dict["user_name"] = user_dict.pop("name")
    user_dict["full_name"] = user_dict["user_name"]
    user_dict["roles"] = user_roles

    token = create_access_token(identity=str(user.id_))
    return {
        "data": {
            "access_token": token,
            "expires_in": 1800,
            # 不需要 refresh_token 了
            # "refresh_token": create_refresh_token(identity=str(user.id_)),
            "roles": user_roles,
            "token_type": "Bearer",
            "user": user_dict,
        },
        "message": "操作成功",
        "success": True,
    }, 200, {"Authorization": f"Bearer {token}"}


def create(username, password, email, real_name, description, role_ids):
    if db.session.query(User).filter_by(name=username).count() > 0:
        return restful.error("用户名已存在")

    roles = db.session.query(Role).filter(Role.id_.in_(role_ids)).all()
    user = User(
        name=username,
        password=password,
        email=email,
        real_name=real_name,
        description=description,
        roles=roles,
    )
    db.session.add(user)
    db.session.commit()
    return restful.success(user.to_dict())


def users(name, page, per_page):
    query = db.session.query(User)
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))

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
    user = db.session.query(User).filter_by(id_=id_).one_or_none()
    user = user and user.to_dict()
    return restful.success(user)


def delete_by_id(id_):
    user = db.session.query(User).filter_by(id_=id_).one_or_none()
    if user:
        db.session.delete(user)
        db.session.commit()

    return restful.success({"id": id_})


def update(id_, username, email, real_name, description, role_ids):
    user = db.session.query(User).filter_by(id_=id_).one_or_none()
    if not user:
        return restful.error("用户不存在")

    user.name = username
    user.email = email
    user.real_name = real_name
    user.description = description
    user.roles = db.session.query(Role).filter(Role.id_.in_(role_ids)).all()
    db.session.commit()
    return restful.success({"id": id_})


def change_password(user_id, password):
    user = db.session.query(User).filter_by(id_=user_id).one_or_none()
    if not user:
        return restful.error("not found user"), 404

    user.password = password
    user.forgot_password = False
    db.session.add(user)
    db.session.commit()
    return restful.success({"user_id": user_id})


def forgot_password(username):
    user = db.session.query(User).filter_by(name=username).one_or_none()
    if not user:
        return restful.error("not found user")

    user.forgot_password = True
    db.session.add(user)
    db.session.commit()
    return restful.success({"username": username})


def has_email(email):
    return bool(db.session.query(User).filter_by(email=email).count())


def has_username(username):
    return bool(db.session.query(User).filter_by(name=username).count())


def register(username, email, dept):
    if db.session.query(User).filter_by(name=username).count() > 0:
        return restful.error("用户名已存在")

    user = User(name=username, email=email, dept=dept, password="")
    db.session.add(user)
    db.session.commit()
    return restful.success(user.to_dict())


def has_username_email(username, email):
    return db.session.query(User).filter_by(name=username, email=email).count()


def change_password_by_username_email(username, email, password):
    user = db.session.query(User).filter_by(name=username, email=email).one_or_none()  # noqa
    if not user:
        return restful.error("not found user"), 404

    user.password = password
    db.session.add(user)
    db.session.commit()
    return restful.success({"username": username, "email": email})

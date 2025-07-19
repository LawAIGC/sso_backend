
import os

import models
from exts import db


def init_db():
    init_menus = [
        {"name": "权限中心"},
        {"name": "云管平台"},
        {"name": "大屏总览"},
        {"name": "资源编排"},
    ]
    if models.Menu.query.count() == 0:
        menus = [models.Menu(**menu) for menu in init_menus]
        db.session.add_all(menus)
        db.session.commit()
    else:
        menus = [
            models.Menu.query.filter_by(name=menu["name"]).one()
            for menu in init_menus
        ]

    init_abilities = [
        {"name": "权限中心", "menus": [menus[0]]},
        {"name": "云管平台", "menus": [menus[1]]},
        {"name": "大屏总览", "menus": [menus[2]]},
        {"name": "资源编排", "menus": [menus[3]]},
    ]
    if models.Ability.query.count() == 0:
        abilities = [models.Ability(**ability) for ability in init_abilities]
        db.session.add_all(abilities)
        db.session.commit()
    else:
        abilities = [
            models.Ability.query.filter_by(name=ability["name"]).one()
            for ability in init_abilities
        ]

    init_roles = [
        {"name": "user", "abilities": [abilities[2]]},
        {"name": "admin", "abilities": abilities}
    ]
    if models.Role.query.count() == 0:
        roles = [models.Role(**role) for role in init_roles]
        db.session.add_all(roles)
        db.session.commit()

    if models.User.query.count() == 0:
        user_role = models.Role.query.filter_by(name="user").one()
        admin_role = models.Role.query.filter_by(name="admin").one()
        init_users = [
            {"name": "user", "roles": [user_role], "password": os.getenv("password", "password")},
            {"name": "admin", "roles": [admin_role], "password": os.getenv("password", "password")}
        ]
        users = [models.User(**user) for user in init_users]
        db.session.add_all(users)
        db.session.commit()

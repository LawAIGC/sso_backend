from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import const
from exts import db

"""
    User <-> Role

    Role <-> Ability

    Ability <-> Menu

"""

UserRoleTable = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
)

RoleAbilityTable = db.Table(
    "role_ability",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("ability_id", db.Integer, db.ForeignKey("ability.id"))
)

AbilityMenuTable = db.Table(
    "ability_menu",
    db.Column("ability_id", db.Integer, db.ForeignKey("ability.id")),
    db.Column("menu_id", db.Integer, db.ForeignKey("menu.id")),
)


class User(db.Model):
    id_ = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    dept = db.Column(db.String(100), nullable=True)
    __password_hash = db.Column("password", db.String(255), nullable=False)
    real_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(255), nullable=True, default=None)
    phone = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=True, default=const.UserStatus.active.name)
    last_login_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)  # noqa
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    forgot_password = db.Column(db.Boolean, nullable=True, default=False)

    roles = db.relationship("Role", secondary=UserRoleTable, back_populates="users")  # noqa

    @property
    def password(self):
        return self.__password_hash

    @password.setter
    def password(self, password):
        self.__password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.__password_hash, password)

    def to_dict(self):
        roles = [role.to_dict() for role in self.roles]
        return {
            "id": self.id_,
            "user_id": self.id_,
            "name": self.name,
            "username": self.name,
            "dept": self.dept,
            "email": self.email,
            "real_name": self.real_name,
            "phone": self.phone,
            "description": self.description,
            "avatar_url": self.avatar_url,
            "status": self.status,
            "forgot_password": self.forgot_password,
            "roles": roles,
            "roleinfos": roles,
            "last_login_at": self.last_login_at.strftime(const.DATETIME_FORMAT) if self.last_login_at else None,  # noqa
            "created_at": self.created_at.strftime(const.DATETIME_FORMAT),
            "updated_at": self.updated_at.strftime(const.DATETIME_FORMAT),
            "deleted_at": self.deleted_at.strftime(const.DATETIME_FORMAT) if self.deleted_at else None,  # noqa
        }

    def get_menus(self):
        return (
            Menu.query
            .join(Menu.abilities)
            .join(Ability.roles)
            .join(Role.users)
            .filter(User.id_ == self.id_)
            .distinct(Menu.id_)
        )


class Role(db.Model):
    id_ = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default=const.RoleStatus.active.name)
    level = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey(id_), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)  # noqa
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    parent = db.relationship("Role", remote_side=[id_], foreign_keys=[parent_id], backref="children")  # noqa

    users = db.relationship(User, secondary=UserRoleTable, back_populates="roles")  # noqa
    abilities = db.relationship("Ability", secondary=RoleAbilityTable, back_populates="roles")

    def get_menus(self):
        return Menu.query.join(Menu.abilities).join(Ability.roles).filter(Role.id_ == self.id_).distinct(Menu.id_)

    def to_dict(self):
        return {
            "role_id": self.id_,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "menus": [
                menu.to_dict()
                for menu in self.get_menus()
            ]
        }


class Ability(db.Model):
    id_ = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    category = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    identifier = db.Column(db.String(100), nullable=True)
    is_system = db.Column(db.Boolean, nullable=True)
    level = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)  # noqa

    roles = db.relationship(Role, secondary=RoleAbilityTable, back_populates="abilities", lazy="dynamic")
    menus = db.relationship("Menu", secondary=AbilityMenuTable, back_populates="abilities")

    def to_dict(self):
        return {
            "id": self.id_,
            "name": self.name,
            "permission": self.name,
            "description": self.description,
            "category": self.category,
            "identifier": self.identifier,
            "enabled": self.enabled,
            "is_system": self.is_system,
            "level": self.level,
            "menus": [menu.to_dict() for menu in self.menus],
            "created_at": self.created_at.strftime(const.DATETIME_FORMAT),
            "updated_at": self.updated_at.strftime(const.DATETIME_FORMAT),
        }


class Menu(db.Model):
    id_ = db.Column("id", db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    pid = db.Column(db.Integer, nullable=True)
    type_ = db.Column("type", db.String(100), nullable=True)
    sort = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)  # noqa
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    abilities = db.relationship(Ability, secondary=AbilityMenuTable, back_populates="menus", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id_,
            "menu_name": self.name,
            "menu_type": self.type_,
            "path": self.path,
            "pid": self.pid,
            "sort": self.sort,
            "created_at": self.created_at.strftime(const.DATETIME_FORMAT),
            "updated_at": self.updated_at.strftime(const.DATETIME_FORMAT),
        }

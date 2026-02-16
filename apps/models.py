# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Page(db.Model):

    __tablename__ = 'Page'

    id = db.Column(db.Integer, primary_key=True)

    #__Page_FIELDS__
    title = db.Column(db.String(255),  nullable=True)
    content = db.Column(db.Text, nullable=True)
    access_level = db.Column(db.String(255),  nullable=True)
    image = db.Column(db.String(255),  nullable=True)

    #__Page_FIELDS__END

    def __init__(self, **kwargs):
        super(Page, self).__init__(**kwargs)


class User(db.Model):

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)

    #__User_FIELDS__
    name = db.Column(db.String(255),  nullable=True)
    email = db.Column(db.String(255),  nullable=True)
    password = db.Column(db.String(255),  nullable=True)
    stripe_member_id = db.Column(db.String(255),  nullable=True)
    stripe_subscription_id = db.Column(db.String(255),  nullable=True)
    user_status = db.Column(db.String(255),  nullable=True)

    #__User_FIELDS__END

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Post(db.Model):

    __tablename__ = 'Post'

    id = db.Column(db.Integer, primary_key=True)

    #__Post_FIELDS__
    title = db.Column(db.String(255),  nullable=True)
    content = db.Column(db.Text, nullable=True)
    page_id = db.Column(db.Integer, nullable=True)
    post_image = db.Column(db.String(255),  nullable=True)

    #__Post_FIELDS__END

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)



#__MODELS__END

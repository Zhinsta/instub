# -*- coding: utf-8 -*-

from instub.database import db, SurrogatePK, Model

from user import iAdmin, User
from media import Category, Worker, Media, WorkerCategory


class SiteSetting(SurrogatePK, Model):

    __tablename__ = 'site_setting'

    name = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    slogan = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())



__all__ = [iAdmin, User, Category, Worker, WorkerCategory, SiteSetting, Media]

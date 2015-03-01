# coding: utf-8

from flask.ext.admin import Admin

from instub.models import User, Category, iAdmin, Worker, SiteSetting, Media
from instub.panel.home import (UserPanel, AdminPanel, CategoryPanel,
                               WorkerPanel, SitePanel, PanelIndex, MediaPanel)
from instub.database import db


iadmin = Admin(name='Instub Admin', index_view=PanelIndex(),
               base_template='my_master.html')
iadmin.add_view(SitePanel(SiteSetting, db.session))
iadmin.add_view(AdminPanel(iAdmin, db.session))
iadmin.add_view(UserPanel())
iadmin.add_view(WorkerPanel())
iadmin.add_view(CategoryPanel(Category, db.session))
iadmin.add_view(MediaPanel(Media, db.session))

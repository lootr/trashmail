#!/usr/bin/env python3
import cherrypy
import os
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin

from trashmail import Root
from trashmail.models import ORMBase

def get_engine_url(conf):
    pattern = "{dialect}"
    if "driver" in conf:
        pattern += "+{driver}"
    pattern += "://"
    if "datasource" in conf:
        pattern += "{datasource}"
    else:
        if "user" in conf:
            pattern += "{user}"
        if "pass" in conf:
            pattern += ":{pass}"
    if "host" in conf:
        pattern += "@{host}"
    if "port" in conf:
        pattern += ":{port}"
    if "database" in conf:
        pattern += "/{database}"

    return pattern.format(**conf)

if __name__ == '__main__':
    cherrypy.tools.db = SQLAlchemyTool()
    cherrypy.config.update("server.conf")

    app = cherrypy.tree.mount(Root(), '/', "app.conf")

    create_kw = {}
    if cherrypy.config.get('debug', False):
        create_kw['echo'] = True

    engine_url = get_engine_url(app.config['db'])
    sap = SQLAlchemyPlugin(cherrypy.engine, ORMBase, engine_url, **create_kw)
    sap.start()
    sap.bind(cherrypy.tools.db.session)
    sap.create()

    cherrypy.engine.start()
    cherrypy.engine.block()

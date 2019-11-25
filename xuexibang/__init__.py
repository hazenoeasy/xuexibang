# -*- coding: utf-8 -*-

import os

import click
from flask import Flask, render_template

from xuexibang.blueprints.auth import auth_bp
from xuexibang.blueprints.front import front_bp
from xuexibang.blueprints.dashboard import dashboard_bp
from xuexibang.main.extensions import bootstrap, db, ckeditor, moment, mail
from xuexibang.settings import config

from database.api.main_base import *

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')  # 从.flaskenv中找FLASK_CONFIG，如果没找到则默认development
    app = Flask('xuexibang')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    # need?
    # db.init_app(app)

    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(front_bp)
    app.register_blueprint(dashboard_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            # 删除所有表并重新建表
            db.get_result({"function": DATABASE_INIT, "content": "","dev":True})
            click.echo('Drop tables.')
        click.echo('Initialized database.')

'''
# success!
o = Operator()
res = o.get_result({"function": DATABASE_INIT, "content": "","dev":True})
print (res)
o.destroy()
'''
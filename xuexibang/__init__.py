# -*- coding: utf-8 -*-

import os

import click
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from xuexibang.blueprints.auth import auth_bp
from xuexibang.blueprints.front import front_bp
from xuexibang.blueprints.dashboard import dashboard_bp
from xuexibang.main.extensions import bootstrap, db, ckeditor, moment, mail, login_manager, csrf
from xuexibang.settings import config


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
    login_manager.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(front_bp)
    app.register_blueprint(dashboard_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


'''模板的上下文变量'''


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        categories = db.get_result({"function": db.GET_ALL_CATEGORY})["content"]  # 用于显示边栏
        unread_questions = len(db.get_result({"function": db.GET_UNREAD_QUESTION, 'content':{
            "start": 0,
            "number": 99
        }})["content"])
        unread_answers = len(db.get_result({"function": db.GET_UNREAD_ANSWER, "content":{
            "start": 0,
            "number": 99
        }})["content"])
        return dict(categories=categories, unread_answers=unread_answers, unread_questions=unread_questions)


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

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            # 删除所有表并重新建表
            db.get_result({"function": db.DATABASE_INIT, "content": "","dev":True})
            click.echo('Drop tables.')
        click.echo('Initialized database.')


    @app.cli.command()
    @click.option('--username', prompt=True, help='The administrator\'s name used to login.')
    @click.option('--email', prompt=True, help='The email:')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, email, password):
        from database.models.model import UserInfo
        click.echo('Initializing the database...')
        db.get_result({"function": db.DATABASE_INIT, "content": "", "dev": True})

        click.echo('Creating the temporary administrator account...')
        admin=UserInfo(name=username, email=email, admin=True)
        admin.set_password(password)
        db.get_result({"function":db.INSERT_USER, "content":admin.to_dict()})
        click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=5, help='Quantity of question\'s categoty, 5 kinds')
    @click.option('--qna', default=10, help='Generate questions and their answers, 10 questions')
    @click.option('--follow', default=1, help='Generate user id=1 \'s follow')
    def forge(category, qna, follow):
        from xuexibang.main.fakes import fake_category, fake_follow, fake_qna, fake_user
        # 初始化数据库放到了init选项中
        # db.get_result({"function": db.DATABASE_INIT, "content": "", "dev":True})

        click.echo('Generating the user..')
        fake_user()

        click.echo('Generating the question\'s %d categoty...' % category)
        fake_category(category)

        click.echo('Generating %d question and answers' % qna)
        fake_qna(qna)

        click.echo('Generating user\'s follow:')
        fake_follow(follow)

        click.echo('Done.')

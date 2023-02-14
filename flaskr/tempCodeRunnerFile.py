def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
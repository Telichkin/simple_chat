import config
import application


if __name__ == '__main__':
    app = application.create(config.DevelopmentConfig)
    app.app_context().push()
    application.db.create_all()
    app.run()

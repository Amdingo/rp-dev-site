import unittest
from flask.cli import FlaskGroup

from project import app, db

cli = FlaskGroup(app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs tests with coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    res = unittest.TextTestRunner(verbosity=2).run(tests)
    if res.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()

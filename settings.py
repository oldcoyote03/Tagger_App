import os
#basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False
if os.environ.get('TDB_COCKROACHDB_PUBLIC_SERVICE_HOST') is not None:
    s = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = s.replace(
        s[ s.find('@')+1 : s.find(':', s.find('@')+1) ], 
        os.environ.get('TDB_COCKROACHDB_PUBLIC_SERVICE_HOST')
    )
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

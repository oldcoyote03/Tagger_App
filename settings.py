import os
#basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# not ideal for app to be aware of infra layer details
# s = os.environ.get('SQLALCHEMY_DATABASE_URI')
# if os.environ.get('TDB_COCKROACHDB_PUBLIC_SERVICE_HOST') is not None:
#     s = s.replace(
#         s[ s.find('@')+1 : s.find(':', s.find('@')+1) ], 
#         os.environ.get('TDB_COCKROACHDB_PUBLIC_SERVICE_HOST')
#     )
# SQLALCHEMY_DATABASE_URI = s

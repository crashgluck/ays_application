try:
    import pymysql
except ImportError:
    # Local sqlite development can run without pymysql installed.
    pymysql = None
else:
    pymysql.install_as_MySQLdb()

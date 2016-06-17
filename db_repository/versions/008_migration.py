from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
message = Table('message', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_username', String(length=64)),
    Column('second_username', String(length=64)),
    Column('chat', String(length=140)),
    Column('timestamp', DateTime),
    Column('chat_by', String(length=64)),
    Column('read_permission_first_user', Boolean, default=ColumnDefault(True)),
    Column('read_permission_second_user', Boolean, default=ColumnDefault(True)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['message'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['message'].drop()

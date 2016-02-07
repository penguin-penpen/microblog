from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR),
    Column('body', VARCHAR),
    Column('timestamp', VARCHAR),
    Column('info', VARCHAR),
    Column('body_markdown', VARCHAR),
    Column('counter', INTEGER),
    Column('lan_used', VARCHAR),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String),
    Column('body', String),
    Column('timestamp', String),
    Column('info', String),
    Column('body_markdown', String),
    Column('counter', Integer),
    Column('lan_used', String),
)

post_tag_rel = Table('post_tag_rel', post_meta,
    Column('tag_rel_id', Integer, primary_key=True, nullable=False),
    Column('tag_id', Integer),
    Column('id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['post'].create()
    post_meta.tables['post_tag_rel'].columns['id'].create()
    post_meta.tables['post_tag_rel'].columns['tag_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['post'].drop()
    post_meta.tables['post_tag_rel'].columns['id'].drop()
    post_meta.tables['post_tag_rel'].columns['tag_id'].drop()

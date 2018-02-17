import sqlalchemy as sa
from . import config
import sqlalchemy.dialects.postgresql as psql

Auth_Backend = sa.Table('auth_backends', config.metadata,
    sa.Column('uuid', psql.UUID, primary_key=True, default=config.uuid),
    sa.Column('name', sa.String(255)),
    sa.Column('settings', sa.JSON),
)

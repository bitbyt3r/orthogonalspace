import sqlalchemy as sa
from . import config
import sqlalchemy.dialects.postgresql as psql

User = sa.Table('users', config.metadata,
    sa.Column('uuid', psql.UUID, primary_key=True, default=config.uuid),
    sa.Column('username', sa.String(255)),
    sa.Column('realname', sa.String(255)),
    sa.Column('email', sa.String(255)),
    sa.Column('auth_backend', sa.ForeignKey('auth_backends.uuid')),
    sa.Column('auth_data', sa.JSON),
)

import sqlalchemy as sa
from . import config
import sqlalchemy.dialects.postgresql as psql

Session = sa.Table('sessions', config.metadata,
    sa.Column('uuid', psql.UUID, primary_key=True, default=config.uuid),
    sa.Column('user', sa.ForeignKey('users.uuid')),
    sa.Column('time', sa.DateTime),
    sa.Column('transport_id', sa.Integer),
)

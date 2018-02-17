import sqlalchemy as sa
from . import config
import sqlalchemy.dialects.postgresql as psql

User_Group_Assoc = sa.Table('user_group_assoc', config.metadata,
    sa.Column('uuid', psql.UUID, primary_key=True, default=config.uuid),
    sa.Column('user', sa.ForeignKey('users.uuid')),
    sa.Column('group', sa.ForeignKey('groups.uuid')),
)

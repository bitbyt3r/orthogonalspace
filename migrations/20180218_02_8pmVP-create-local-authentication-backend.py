"""
Create local authentication backend
"""

from yoyo import step

__depends__ = {'20180218_01_FjwIl-add-initial-tables'}

steps = [
step("""
INSERT INTO auth_backends (uuid, name) VALUES (uuid_generate_v4(), 'Local')
""", """DELETE FROM auth_backends WHERE name='Local' """)
]

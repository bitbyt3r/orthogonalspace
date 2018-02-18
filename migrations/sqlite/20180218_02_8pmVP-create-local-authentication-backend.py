"""
Create local authentication backend
"""

from yoyo import step

__depends__ = {'20180218_01_FjwIl-add-initial-tables'}

steps = [
step("""
INSERT INTO auth_backends (uuid, name) VALUES ((lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || '-' || lower(hex(randomblob(6)))), 'Local')
""", """DELETE FROM auth_backends WHERE name='Local' """)
]

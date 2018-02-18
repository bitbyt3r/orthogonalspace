"""
Add initial tables
"""

from yoyo import step

__depends__ = {}

steps = [
step("""
CREATE TABLE auth_backends (
	uuid UUID NOT NULL, 
	name VARCHAR(255), 
	settings JSON, 
	PRIMARY KEY (uuid)
)

""", """DROP TABLE auth_backends"""),
step("""
CREATE TABLE users (
	uuid UUID NOT NULL, 
	username VARCHAR(255), 
	realname VARCHAR(255), 
	email VARCHAR(255), 
	auth_backend UUID, 
	auth_data JSON, 
	PRIMARY KEY (uuid), 
	FOREIGN KEY(auth_backend) REFERENCES auth_backends (uuid)
)

""", """DROP TABLE users"""),
step("""
CREATE TABLE sessions (
	uuid UUID NOT NULL, 
	"user" UUID, 
	time TIMESTAMP WITHOUT TIME ZONE, 
	transport_id INTEGER, 
	PRIMARY KEY (uuid), 
	FOREIGN KEY("user") REFERENCES users (uuid)
)

""", """DROP TABLE sessions"""),

step("""
CREATE TABLE settings (
	uuid UUID NOT NULL, 
	key VARCHAR(255), 
	value VARCHAR(255), 
	PRIMARY KEY (uuid)
)

""", """DROP TABLE settings""")
]

from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean

from app.database import Base


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.now)
    priority = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)


# user = Table(
#     "user",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("username", String, nullable=False),
#     Column("password", String, nullable=False),
#     Column("registered_at", TIMESTAMP, default=datetime.utcnow),
#     Column("role_id", Integer, ForeignKey("role.id"))
# )

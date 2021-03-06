import uuid

import jwt
import pendulum
from passlib.hash import argon2
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy import BigInteger, Boolean, Column, DateTime
from config import get_config
from models.base import Base

app_config = get_config()


class User(Base):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True)
    firstName = Column(VARCHAR, nullable=True, default=None)
    lastName = Column(VARCHAR, nullable=True, default=None)
    emailAddress = Column(VARCHAR, unique=True, nullable=False)
    password = Column(VARCHAR, nullable=False)
    createdTime = Column(DateTime, nullable=False)
    modifiedTime = Column(DateTime, nullable=False)
    UUID = Column(UUID(as_uuid=True), nullable=False)
    phoneNumber = Column(VARCHAR, nullable=True, default=None)
    isVerified = Column(Boolean, nullable=False, default=False)
    userRole = Column(VARCHAR, nullable=False, default="USER")

    def __init__(
        self,
        emailAddress,
        password,
        firstName=None,
        lastName=None,
        phoneNumber=None,
        userRole="USER",
        isVerified=False,
    ):
        now = pendulum.now("UTC")
        self.firstName = firstName
        self.lastName = lastName
        self.emailAddress = emailAddress
        self.password = password
        self.phoneNumber = phoneNumber
        self.userRole = userRole
        self.isVerified = isVerified
        self.createdTime = now
        self.modifiedTime = now
        self.UUID = uuid.uuid4()

    def __str__(self):
        return "id: {} email: {}".format(self.id, self.emailAddress)

    def gen_token(self, expire_hours=app_config.TOKEN_TTL_HOURS):
        payload = {
            "userId": self.id,
            "exp": pendulum.now("UTC").add(hours=int(expire_hours)),
        }
        return str(
            jwt.encode(payload, app_config.JWT_SECRET, app_config.JWT_ALGORITHM).decode(
                "utf-8"
            )
        )

    def pass_matches(self, postPass):
        return argon2.verify(postPass, self.password)

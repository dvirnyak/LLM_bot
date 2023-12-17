from bot import bot
from config import db_engine, db_meta
import sqlalchemy as db
from models import *


if __name__ == "__main__":
    db.MetaData.reflect(db_meta, bind=db_engine)
    Base.metadata.create_all(bind=db_engine)

    bot()
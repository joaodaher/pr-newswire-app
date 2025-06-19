from storage.mongo import get_database

MongoRepository = get_database()

__all__ = ["MongoRepository"]

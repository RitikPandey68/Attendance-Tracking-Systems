from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from typing import Optional
import logging
from core.config import settings, ATTENDANCE_DB, USERS_COLLECTION, STUDENTS_COLLECTION, FACULTY_COLLECTION, ATTENDANCE_COLLECTION, RESULTS_COLLECTION

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        
    def connect(self):
        try:
            self.client = MongoClient(settings.MONGODB_URL)
            self.db = self.client[ATTENDANCE_DB]
            # Test connection
            self.client.admin.command('ping')
            logger.info("Connected to MongoDB successfully")
            self._create_indexes()
            return True
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
            
    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
            
    def _create_indexes(self):
        """Create necessary indexes for optimal performance"""
        try:
            # Users collection indexes
            self.db[USERS_COLLECTION].create_index("email", unique=True)
            
            # Students collection indexes
            self.db[STUDENTS_COLLECTION].create_index("usn", unique=True)
            self.db[STUDENTS_COLLECTION].create_index("email", unique=True)
            self.db[STUDENTS_COLLECTION].create_index("user_id", unique=True)
            
            # Faculty collection indexes
            self.db[FACULTY_COLLECTION].create_index("email", unique=True)
            self.db[FACULTY_COLLECTION].create_index("user_id", unique=True)
            
            # Attendance collection indexes
            self.db[ATTENDANCE_COLLECTION].create_index([("student_id", 1), ("date", 1), ("period", 1)], unique=True)
            self.db[ATTENDANCE_COLLECTION].create_index("date")
            self.db[ATTENDANCE_COLLECTION].create_index("student_id")
            
            # Results collection indexes
            self.db[RESULTS_COLLECTION].create_index([("student_id", 1), ("test_date", 1), ("subject", 1)], unique=True)
            self.db[RESULTS_COLLECTION].create_index("student_id")
            self.db[RESULTS_COLLECTION].create_index("test_date")
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating database indexes: {e}")
            
    def get_collection(self, collection_name: str):
        """Get a specific collection from the database"""
        if self.db is None:
            self.connect()
        return self.db[collection_name]

# Global database instance
db_instance = Database()

def get_db():
    """Get the database instance"""
    if db_instance.db is None:
        db_instance.connect()
    return db_instance

def get_database():
    """Get the database connection"""
    if db_instance.db is None:
        db_instance.connect()
    return db_instance.db

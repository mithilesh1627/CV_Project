"""
MongoDB Inquiry Repository.
Handles persistent storage of contact inquiries in MongoDB Atlas 'contact_inquiries' collection.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import pymongo
from bson import ObjectId
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError, ConnectionFailure

logger = logging.getLogger(__name__)


class InquiryRepository:
    """Repository handling all MongoDB operations for visitor contact inquiries."""

    def __init__(self, mongo_uri: str = "", db_name: str = "portfolio", client: Optional[pymongo.MongoClient] = None):
        self.mongo_uri = mongo_uri.strip() if mongo_uri else ""
        self.db_name = db_name or "portfolio"
        self._client = client

    def _get_client(self) -> Optional[pymongo.MongoClient]:
        """Get or initialize the MongoClient with a fast connection timeout."""
        if self._client is not None:
            return self._client

        if not self.mongo_uri:
            return None

        try:
            self._client = pymongo.MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=4000,
                connectTimeoutMS=4000,
                socketTimeoutMS=4000,
                appName="PortfolioCMS"
            )
            self._client.admin.command("ping")
            return self._client
        except (ServerSelectionTimeoutError, ConnectionFailure, PyMongoError) as err:
            logger.warning("MongoDB unavailable for inquiries. Error: %s", type(err).__name__)
            self._client = None
            return None

    def get_collection(self):
        """Return the 'contact_inquiries' MongoDB collection, or None if unavailable."""
        client = self._get_client()
        if client is None:
            return None
        return client[self.db_name]["contact_inquiries"]

    def save_inquiry(self, name: str, email: str, message: str, ip_address: str = "") -> tuple[bool, Optional[str]]:
        """
        Persist a contact inquiry document into MongoDB.
        Returns (success: bool, inquiry_id: str | None).
        """
        col = self.get_collection()
        if col is None:
            logger.warning("Unable to save inquiry to MongoDB: collection unavailable.")
            return False, None

        doc = {
            "name": name.strip(),
            "email": email.strip(),
            "message": message.strip(),
            "ip_address": ip_address.strip() if ip_address else "",
            "read": False,
            "created_at": datetime.now(timezone.utc),
        }

        try:
            result = col.insert_one(doc)
            inquiry_id = str(result.inserted_id)
            logger.info("Saved contact inquiry %s from '%s' <%s>", inquiry_id, name, email)
            return True, inquiry_id
        except PyMongoError as exc:
            logger.error("Failed to insert contact inquiry into MongoDB: %s", exc)
            return False, None

    def get_inquiries(self, limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        """Fetch inquiries sorted by creation date descending."""
        col = self.get_collection()
        if col is None:
            return []

        try:
            cursor = col.find().sort("created_at", pymongo.DESCENDING).skip(skip).limit(limit)
            inquiries = []
            for doc in cursor:
                doc["id"] = str(doc["_id"])
                # Format datetime string for template display
                if isinstance(doc.get("created_at"), datetime):
                    doc["created_at_formatted"] = doc["created_at"].strftime("%b %d, %Y %I:%M %p UTC")
                else:
                    doc["created_at_formatted"] = str(doc.get("created_at", ""))
                inquiries.append(doc)
            return inquiries
        except PyMongoError as exc:
            logger.error("Failed to fetch inquiries from MongoDB: %s", exc)
            return []

    def get_unread_count(self) -> int:
        """Return count of unread inquiries."""
        col = self.get_collection()
        if col is None:
            return 0
        try:
            return col.count_documents({"read": False})
        except PyMongoError as exc:
            logger.error("Failed to count unread inquiries: %s", exc)
            return 0

    def mark_as_read(self, inquiry_id: str) -> bool:
        """Mark an inquiry as read."""
        col = self.get_collection()
        if col is None or not inquiry_id:
            return False
        try:
            res = col.update_one({"_id": ObjectId(inquiry_id)}, {"$set": {"read": True}})
            return res.modified_count > 0
        except Exception as exc:
            logger.error("Failed to mark inquiry %s as read: %s", inquiry_id, exc)
            return False

    def delete_inquiry(self, inquiry_id: str) -> bool:
        """Delete an inquiry by ID."""
        col = self.get_collection()
        if col is None or not inquiry_id:
            return False
        try:
            res = col.delete_one({"_id": ObjectId(inquiry_id)})
            return res.deleted_count > 0
        except Exception as exc:
            logger.error("Failed to delete inquiry %s: %s", inquiry_id, exc)
            return False

# import chromadb
# from chromadb.utils import embedding_functions
# from config import Config
# from utils.logger import logger
# import hashlib
# from datetime import datetime

# class VersionDB:
#     def __init__(self):
#         self.client = chromadb.PersistentClient(path=Config.DB_PATH)
#         self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
#             model_name="all-MiniLM-L6-v2"
#         )
        
#         self.collection = self.client.get_or_create_collection(
#             name=Config.COLLECTION_NAME,
#             embedding_function=self.embedding_func
#         )
        
#     # def store_version(self, chapter_data):
#     #     """Store a new version of a chapter with validated metadata"""
#     #     try:
#     #         # Generate unique ID
#     #         content_hash = hashlib.md5(chapter_data["content"].encode()).hexdigest()
#     #         version_id = f"{chapter_data['chapter_name']}_{content_hash}"
            
#     #         # Prepare and validate metadata
#     #         metadata = {
#     #             "chapter": str(chapter_data.get("chapter_name", "unknown")),
#     #             "version": str(chapter_data.get("version", "1.0")),
#     #             "status": str(chapter_data.get("status", "draft")),
#     #             "author": str(chapter_data.get("author", "ai_writer")),
#     #             "timestamp": str(chapter_data.get("timestamp", datetime.now().isoformat())),
#     #             "source_url": str(chapter_data.get("source_url", "")),
#     #             "screenshot": str(chapter_data.get("screenshot", "")),
#     #             "human_feedback": str(chapter_data.get("human_feedback", ""))
#     #         }
            
#     #         # Ensure no None values remain
#     #         metadata = {k: "" if v == "None" else v for k, v in metadata.items()}
            
#     #         # Store in ChromaDB
#     #         self.collection.add(
#     #             documents=[chapter_data["content"]],
#     #             metadatas=[metadata],
#     #             ids=[version_id]
#     #         )
            
#     #         logger.info(f"Stored version {version_id}")
#     #         return version_id
            
#     #     except Exception as e:
#     #         logger.error(f"Failed to store version: {str(e)}")
#     #         raise
#     def store_version(self, chapter_data):
#         """Store a new version of a chapter with duplicate checking"""
#         try:
#             content_hash = hashlib.md5(chapter_data["content"].encode()).hexdigest()
#             version_id = f"{chapter_data['chapter_name']}_{content_hash}"
            
#             # Check for existing version
#             existing = self.collection.get(ids=[version_id])
#             if existing["documents"]:
#                 logger.info(f"Version {version_id} already exists - updating metadata")
                
#             metadata = {
#                 "chapter": str(chapter_data.get("chapter_name", "unknown")),
#                 "version": str(chapter_data.get("version", "1.0")),
#                 "status": str(chapter_data.get("status", "draft")),
#                 "author": str(chapter_data.get("author", "ai_writer")),
#                 "timestamp": str(chapter_data.get("timestamp", datetime.now().isoformat())),
#                 "source_url": str(chapter_data.get("source_url", "")),
#                 "screenshot": str(chapter_data.get("screenshot", "")),
#                 "human_feedback": str(chapter_data.get("human_feedback", ""))
#             }
            
#             self.collection.upsert(
#                 documents=[chapter_data["content"]],
#                 metadatas=[metadata],
#                 ids=[version_id]
#             )
            
#             logger.info(f"Stored version {version_id}")
#             return version_id
            
#         except Exception as e:
#             logger.error(f"Failed to store version: {str(e)}")
#             raise
    
#     def get_version(self, version_id):
#         """Retrieve a specific version"""
#         try:
#             result = self.collection.get(ids=[version_id])
#             if not result["documents"]:
#                 return None
                
#             return {
#                 "content": result["documents"][0],
#                 "metadata": result["metadatas"][0]
#             }
#         except Exception as e:
#             logger.error(f"Failed to retrieve version: {str(e)}")
#             raise


import chromadb
from chromadb.utils import embedding_functions
from config import Config
from utils.logger import logger
import hashlib
from datetime import datetime

class VersionDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.DB_PATH)
        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            embedding_function=self.embedding_func
        )

    def store_version(self, chapter_data):
        """Store/update a chapter version with metadata"""
        try:
            content_hash = hashlib.md5(chapter_data["content"].encode()).hexdigest()
            version_id = f"{chapter_data['chapter_name']}_{content_hash}"
            
            metadata = {
                "chapter": str(chapter_data.get("chapter_name", "unknown")),
                "version": str(chapter_data.get("version", "1.0")),
                "status": str(chapter_data.get("status", "draft")),
                "author": str(chapter_data.get("author", "ai_writer")),
                "timestamp": str(chapter_data.get("timestamp", datetime.now().isoformat())),
                "source_url": str(chapter_data.get("source_url", "")),
                "screenshot": str(chapter_data.get("screenshot", "")),
                "human_feedback": str(chapter_data.get("human_feedback", ""))
            }
            
            self.collection.upsert(
                documents=[chapter_data["content"]],
                metadatas=[metadata],
                ids=[version_id]
            )
            return version_id
            
        except Exception as e:
            logger.error(f"Failed to store version: {str(e)}")
            raise

    def search_versions(self, query, chapter_name=None, limit=5):
        """Search versions with optional chapter filter"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where={"chapter": chapter_name} if chapter_name else None
            )
            return [{
                "content": doc,
                "metadata": meta,
                "distance": dist
            } for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )]
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []

    def get_version(self, version_id):
        """Retrieve a specific version"""
        try:
            result = self.collection.get(ids=[version_id])
            return {
                "content": result["documents"][0],
                "metadata": result["metadatas"][0]
            } if result["documents"] else None
        except Exception as e:
            logger.error(f"Failed to retrieve version: {str(e)}")
            raise
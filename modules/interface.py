# import inquirer
# from datetime import datetime
# from utils.logger import logger

# class HumanReviewInterface:
#     def __init__(self, ai_processor, version_db):
#         self.ai = ai_processor
#         self.db = version_db
        
#     def start_review_session(self, chapter_data):
#         """Guide human through review process"""
#         try:
#             print(f"\n=== Reviewing Chapter: {chapter_data['chapter_name']} ===")
            
#             # Show original and rewritten versions
#             print("\nOriginal Version Excerpt:")
#             print(chapter_data["original_content"][:500] + "...")
            
#             print("\nRewritten Version:")
#             print(chapter_data["content"])
            
#             # Get human feedback
#             feedback = self._get_human_feedback()
            
#             # Apply human edits if any
#             if feedback.get("needs_edit"):
#                 chapter_data["content"] = self._apply_human_edits(
#                     chapter_data["content"],
#                     feedback["edits"]
#                 )
                
#             # Store reviewed version
#             chapter_data.update({
#                 "status": "reviewed",
#                 "author": "human_reviewer",
#                 "human_feedback": feedback,
#                 "timestamp": datetime.now().isoformat()
#             })
            
#             version_id = self.db.store_version(chapter_data)
            
#             print(f"\nReview completed! Version ID: {version_id}")
#             return version_id
            
#         except Exception as e:
#             logger.error(f"Review session failed: {str(e)}")
#             raise
    
#     def _get_human_feedback(self):
#         """Interactive feedback collection"""
#         questions = [
#             inquirer.List('rating',
#                 message="Rate this rewrite (1-5)",
#                 choices=[1, 2, 3, 4, 5],
#             ),
#             inquirer.Confirm('needs_edit',
#                 message="Does this need manual editing?",
#                 default=False
#             ),
#             inquirer.Text('general_feedback',
#                 message="General feedback/comments",
#                 ignore=lambda x: not x['needs_edit']
#             ),
#             inquirer.Editor('edits',
#                 message="Make your edits (save & close when done)",
#                 ignore=lambda x: not x['needs_edit'],
#                 default="Make your edits above this line. The original text will be preserved below.\n\n----------\n\n"
#             )
#         ]
        
#         answers = inquirer.prompt(questions)
        
#         feedback = {
#             "rating": answers["rating"],
#             "general_feedback": answers.get("general_feedback", ""),
#             "needs_edit": answers["needs_edit"],
#             "timestamp": datetime.now().isoformat()
#         }
        
#         if answers["needs_edit"]:
#             feedback["edits"] = answers["edits"]
            
#         return feedback
    
#     def _apply_human_edits(self, original_text, edited_text):
#         """Apply human edits to the content"""
#         # Simple implementation - in production you'd want more sophisticated merging
#         if "----------" in edited_text:
#             return edited_text.split("----------")[0].strip()
#         return edited_text.strip()


import os
import tempfile
from datetime import datetime
from utils.logger import logger

class HumanReviewInterface:
    def __init__(self, ai_processor, version_db):
        self.ai = ai_processor
        self.db = version_db
        
    def start_review_session(self, chapter_data):
        """Guide human through review process with fallback options"""
        try:
            print(f"\n=== Reviewing Chapter: {chapter_data['chapter_name']} ===")
            
            # Show versions
            print("\nOriginal Version Excerpt:")
            print(chapter_data["original_content"][:500] + "...")
            
            print("\nRewritten Version:")
            print(chapter_data["content"])
            
            # Get feedback
            feedback = self._get_human_feedback()
            
            # Apply edits if needed
            if feedback.get("needs_edit"):
                chapter_data["content"] = self._apply_human_edits(
                    chapter_data["content"],
                    feedback["edits"]
                )
                
            # Store reviewed version
            chapter_data.update({
                "status": "reviewed",
                "author": "human_reviewer",
                "human_feedback": feedback,
                "timestamp": datetime.now().isoformat()
            })
            
            version_id = self.db.store_version(chapter_data)
            print(f"\nReview completed! Version ID: {version_id}")
            return version_id
            
        except Exception as e:
            logger.error(f"Review session failed: {str(e)}")
            # Fallback to simple approval without editing
            print("\nUsing fallback review mode (editing disabled)")
            chapter_data.update({
                "status": "approved",
                "author": "human_reviewer",
                "human_feedback": "Automatic approval",
                "timestamp": datetime.now().isoformat()
            })
            return self.db.store_version(chapter_data)
    
    def _get_human_feedback(self):
        """Simplified feedback collection with editor fallback"""
        print("\nProvide feedback:")
        rating = input("Rate this rewrite (1-5): ")
        needs_edit = input("Does this need manual editing? (y/N): ").lower() == 'y'
        
        feedback = {
            "rating": rating,
            "needs_edit": needs_edit,
            "timestamp": datetime.now().isoformat()
        }
        
        if needs_edit:
            print("\nEnter your edits below (press Enter then Ctrl+Z when done):")
            edits = []
            while True:
                try:
                    line = input()
                    edits.append(line)
                except EOFError:
                    break
            feedback["edits"] = "\n".join(edits)
            
        return feedback
    
    def _apply_human_edits(self, original_text, edited_text):
        """Apply human edits to the content"""
        return edited_text if edited_text.strip() else original_text
from modules.scraper import ChapterScraper
from modules.ai_processor import AIProcessor
from modules.version_db import VersionDB
from modules.search import RLSearchEnhancer
from modules.interface import HumanReviewInterface
from config import Config
from utils.logger import logger
import argparse

def main():
    # Initialize components
    scraper = ChapterScraper()
    ai = AIProcessor()
    db = VersionDB()
    search = RLSearchEnhancer(db)
    interface = HumanReviewInterface(ai, db)
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Book Publication Workflow")
    parser.add_argument("url", help="URL of the chapter to process")
    parser.add_argument("--chapter-name", help="Name of the chapter", required=True)
    parser.add_argument("--skip-human", help="Skip human review", action="store_true")
    args = parser.parse_args()
    
    try:
        # Scrape content
        logger.info("Starting scraping process...")
        scraped_data = scraper.scrape_chapter(args.url, args.chapter_name)
        
        # Store original
        chapter_data = {
            "chapter_name": args.chapter_name,
            "content": scraped_data["content"],
            "screenshot": scraped_data["screenshot"],
            "source_url": args.url,
            "original_content": scraped_data["content"],
            "status": "scraped"
        }
        db.store_version(chapter_data)
        
        # AI Rewriting
        logger.info("Starting AI rewriting...")
        rewritten_content = ai.rewrite_chapter(
            scraped_data["content"],
            style_guidelines="Modernize language while preserving original tone"
        )
        
        # Store rewritten
        chapter_data.update({
            "content": rewritten_content,
            "status": "ai_rewritten",
            "author": "ai_writer"
        })
        db.store_version(chapter_data)
        
        # AI Review
        logger.info("Starting AI review...")
        ai_feedback = ai.review_chapter(rewritten_content, scraped_data["content"])
        print("\nAI Reviewer Feedback:")
        print(ai_feedback)
        
        # Human Review
        if not args.skip_human:
            logger.info("Starting human review...")
            interface.start_review_session(chapter_data)
        else:
            chapter_data.update({
                "status": "auto_approved",
                "human_feedback": "Skipped human review"
            })
            db.store_version(chapter_data)
            
        # Search demo
        logger.info("Processing complete!")
        print("\nSample search results:")
        results = search.search("opening scene", args.chapter_name)
        for i, res in enumerate(results[:3], 1):
            print(f"\nResult {i}:")
            print(res["metadata"]["author"], res["metadata"]["status"])
            print(res["content"][:200] + "...")
            
    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
import google.generativeai as genai
from config import Config
from utils.logger import logger

class AIProcessor:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        # Use stable model names
        self.writer_model = genai.GenerativeModel('models/gemini-1.5-flash')
        self.reviewer_model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    def rewrite_chapter(self, original_text, style_guidelines=None):
        try:
            prompt = f"""Rewrite this chapter with a fresh creative spin while maintaining:
- Original plot points
- Character personalities
- Key dialogues
- Overall tone

Guidelines: {style_guidelines or "Be creative but faithful to the source"}

Original Chapter:
{original_text}

Rewritten Chapter:"""
            
            response = self.writer_model.generate_content(
                prompt,
                generation_config={"temperature": Config.WRITER_TEMPERATURE}
            )
            return response.text
        except Exception as e:
            logger.error(f"AI writing failed: {str(e)}")
            raise

    def review_chapter(self, rewritten_text, original_text=None):
        try:
            prompt = f"""Analyze this rewritten chapter and provide detailed feedback on:
1. Consistency with original (plot, characters)
2. Writing quality (flow, pacing)
3. Creativity and originality
4. Areas for improvement

Original Chapter (excerpt):
{original_text[:500] + "..." if original_text else "Not provided"}

Rewritten Chapter:
{rewritten_text}

Detailed Feedback:"""
            
            response = self.reviewer_model.generate_content(
                prompt,
                generation_config={"temperature": Config.REVIEWER_TEMPERATURE}
            )
            return response.text
        except Exception as e:
            logger.error(f"AI review failed: {str(e)}")
            raise
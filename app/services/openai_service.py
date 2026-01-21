from openai import OpenAI
from app.config import settings
from app.schemas import WelcomeMessageRequest, DocumentSummarizeRequest
from typing import Optional


class OpenAIService:
    def __init__(self):
        if settings.openai_api_key:
            self.client = OpenAI(api_key=settings.openai_api_key)
        else:
            self.client = None

    async def generate_welcome_message(
        self, 
        intern_name: str, 
        intern_email: str, 
        start_date: str,
        department: Optional[str] = None,
        mentor_name: Optional[str] = None,
        custom_message: Optional[str] = None
    ) -> str:
        """Generate a personalized welcome message for a new intern"""
        if not self.client:
            return self._default_welcome_message(intern_name, start_date)

        prompt = f"""Generate a warm, professional, and personalized welcome message for a new intern.

Intern Details:
- Name: {intern_name}
- Email: {intern_email}
- Start Date: {start_date}
"""
        if department:
            prompt += f"- Department: {department}\n"
        if mentor_name:
            prompt += f"- Mentor: {mentor_name}\n"
        if custom_message:
            prompt += f"\nAdditional context: {custom_message}\n"

        prompt += """
Please create a welcoming message that:
1. Greets them by name
2. Expresses excitement about them joining
3. Mentions their start date
4. If mentor is provided, mentions their mentor
5. Sets a positive tone for their onboarding journey
6. Is concise (2-3 paragraphs)

Write the message in a friendly but professional tone."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates welcoming messages for new employees."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating welcome message: {e}")
            return self._default_welcome_message(intern_name, start_date)

    async def summarize_document(self, document_text: str, max_length: int = 200) -> str:
        """Summarize a document using OpenAI"""
        if not self.client:
            return self._default_summary(document_text, max_length)

        prompt = f"""Please provide a concise summary of the following document in approximately {max_length} words or less:

{document_text}

Summary:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise summaries of documents."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length + 50,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error summarizing document: {e}")
            return self._default_summary(document_text, max_length)

    def _default_welcome_message(self, name: str, start_date: str) -> str:
        """Fallback welcome message if OpenAI is not available"""
        return f"""Dear {name},

Welcome to our team! We are thrilled to have you join us starting on {start_date}.

We're excited about the contributions you'll make and look forward to supporting you throughout your onboarding journey. If you have any questions, please don't hesitate to reach out.

Best regards,
The Onboarding Team"""

    def _default_summary(self, text: str, max_length: int) -> str:
        """Fallback summary if OpenAI is not available"""
        words = text.split()
        if len(words) <= max_length:
            return text
        return " ".join(words[:max_length]) + "..."


# Singleton instance
openai_service = OpenAIService()

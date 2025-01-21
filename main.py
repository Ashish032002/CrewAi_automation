# financial_news_crew.py
import os
from datetime import datetime, timedelta
from typing import Dict, List
import json
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import schedule
import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from brevo_sdk import BrevoAPIClient
import telegram
import litellm

# Load environment variables
load_dotenv()

# Configure LiteLLM for Hugging Face
litellm.set_api_key(os.getenv("HUGGINGFACE_API_KEY"))
# Set Hugging Face as the default provider
litellm.set_model_default_provider("huggingface")

class FinancialNewsTools:
    @staticmethod
    def search_financial_news(hours_ago: int = 1) -> List[Dict]:
        """Search for recent financial news using various APIs"""
        try:
            # Implement your preferred search API here (SERP API, Tavily, etc.)
            news_data = [
                {
                    "title": "Sample Financial News",
                    "source": "Example Source",
                    "timestamp": datetime.now().isoformat(),
                    "url": "https://example.com/news"
                }
            ]
            return news_data
        except Exception as e:
            print(f"Error searching news: {e}")
            return []

    @staticmethod
    def save_to_json(data: List[Dict], filename: str = "financial_news.json"):
        """Save news data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving to JSON: {e}")

    @staticmethod
    def generate_pdf(content: str, language: str, filename: str):
        """Generate PDF report with proper styling"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom style for RTL text if needed
        if language == "Hebrew":
            rtl_style = ParagraphStyle(
                'RTL',
                parent=styles['Normal'],
                alignment=2,  # right alignment
                fontName='Hebrew',
                fontSize=12
            )
            styles.add(rtl_style)
            
        story = []
        story.append(Paragraph(content, 
                             styles['RTL'] if language == "Hebrew" else styles['Normal']))
        doc.build(story)

    @staticmethod
    def send_report(file_path: str, method: str = "email"):
        """Send report via email or Telegram"""
        try:
            if method == "email":
                # Initialize Brevo client
                client = BrevoAPIClient(api_key=os.getenv("BREVO_API_KEY"))
                # Implement email sending logic
                pass
            elif method == "telegram":
                # Initialize Telegram bot
                bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
                # Implement telegram sending logic
                pass
        except Exception as e:
            print(f"Error sending report: {e}")

class FinancialNewsCrew:
    def __init__(self):
        self.tools = FinancialNewsTools()
        
        # Initialize agents with Hugging Face models
        self.news_collector = Agent(
            role='Financial News Collector',
            goal='Collect and organize recent financial news',
            backstory='Expert at gathering and organizing financial news from various sources',
            tools=[self.tools.search_financial_news, self.tools.save_to_json],
            llm_model="huggingface/mistralai/Mixtral-8x7B-Instruct-v0.1"  # Using Mixtral model
        )
        
        self.news_analyzer = Agent(
            role='Financial News Analyzer',
            goal='Create comprehensive summaries of financial news',
            backstory='Expert financial analyst who creates clear and insightful summaries',
            llm_model="huggingface/meta-llama/Llama-2-70b-chat-hf"  # Using Llama 2
        )
        
        self.translator = Agent(
            role='Content Translator',
            goal='Translate content into multiple languages accurately',
            backstory='Expert translator specializing in financial content',
            tools=[self.tools.generate_pdf],
            llm_model="huggingface/facebook/mbart-large-50-many-to-many-mmt"  # Using mBART for translation
        )
        
        self.distributor = Agent(
            role='Report Distributor',
            goal='Ensure reports are properly distributed to all channels',
            backstory='Expert in digital content distribution',
            tools=[self.tools.send_report],
            llm_model="huggingface/mistralai/Mixtral-8x7B-Instruct-v0.1"
        )

    def run_workflow(self):
        """Execute the complete news aggregation and distribution workflow"""
        try:
            # Create tasks
            collect_news = Task(
                description="Collect last hour's financial news and save to JSON",
                agent=self.news_collector
            )

            analyze_news = Task(
                description="Create 500-word summary of collected news",
                agent=self.news_analyzer
            )

            translate_content = Task(
                description="Translate summary to Hindi, Tamil, and Hebrew",
                agent=self.translator
            )

            distribute_reports = Task(
                description="Send reports via email and Telegram",
                agent=self.distributor
            )

            # Create and run crew
            crew = Crew(
                agents=[self.news_collector, self.news_analyzer, 
                       self.translator, self.distributor],
                tasks=[collect_news, analyze_news, translate_content, 
                       distribute_reports],
                process=Process.sequential
            )

            result = crew.kickoff()
            return result
            
        except Exception as e:
            print(f"Error in workflow: {e}")
            # Add proper logging here

def main():
    crew = FinancialNewsCrew()
    
    def job():
        print(f"Starting job at {datetime.now()}")
        crew.run_workflow()
    
    # Schedule job for 16:30 EST daily
    schedule.every().day.at("16:30").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

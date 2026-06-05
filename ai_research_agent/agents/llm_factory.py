import os
import json
import re
from typing import Dict, Any

class LLMFactory:
    def __init__(self, provider: str = "gemini", model_name: str = None):
        self.provider = provider.lower()
        
        if self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model = genai.GenerativeModel(model_name or "gemini-1.5-flash")
        else:
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model_name = model_name or "gpt-3.5-turbo"
    
    def generate(self, prompt: str) -> str:
        if self.provider == "gemini":
            response = self.model.generate_content(prompt)
            return response.text
        else:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
    
    def analyze_company(self, research_data: Dict) -> Dict:
        company = research_data['company_name']
        info = research_data['basic_info']
        
        prompt = f"""
        Analyze {company} and return JSON:
        
        Company Info: {info}
        
        Return EXACT JSON format:
        {{
            "challenges": {{
                "operational": ["challenge1", "challenge2", "challenge3"],
                "sales": ["challenge1", "challenge2"],
                "customer": ["challenge1", "challenge2"],
                "reasoning": "brief explanation"
            }},
            "ai_opportunities": {{
                "automation": ["opportunity1", "opportunity2"],
                "customer_engagement": ["opportunity1", "opportunity2"],
                "sales": ["opportunity1", "opportunity2"],
                "operations": ["opportunity1", "opportunity2"],
                "analytics": ["opportunity1", "opportunity2"],
                "document_processing": ["opportunity1", "opportunity2"]
            }}
        }}
        
        Make it specific to {company}'s industry.
        """
        
        try:
            response = self.generate(prompt)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback
        return {
            "challenges": {
                "operational": ["Process inefficiencies", "Manual workflows", "Data silos"],
                "sales": ["Lead conversion", "Customer acquisition cost"],
                "customer": ["Response time", "Personalization"],
                "reasoning": f"Based on {company}'s industry analysis"
            },
            "ai_opportunities": {
                "automation": ["Automate document processing", "Workflow automation"],
                "customer_engagement": ["AI chatbot", "Personalized recommendations"],
                "sales": ["Lead scoring", "Sales forecasting"],
                "operations": ["Process optimization", "Resource planning"],
                "analytics": ["Business intelligence", "Customer insights"],
                "document_processing": ["Contract analysis", "Data extraction"]
            }
        }
    
    def generate_pitch(self, company_name: str, analysis: Dict) -> str:
        prompt = f"""
        Write a one-page CEO pitch for {company_name}.
        
        Challenges: {analysis.get('challenges', {})}
        Opportunities: {analysis.get('ai_opportunities', {})}
        
        Make it professional, specific to {company_name}, and action-oriented.
        Include: opening, 3 opportunities, 90-day pilot, next steps.
        """
        
        try:
            return self.generate(prompt)
        except:
            return f"""
            DATE: Current Date
            TO: CEO, {company_name}
            FROM: AI Solutions Consultant
            
            Dear CEO,
            
            I'm reaching out about AI opportunities for {company_name}.
            
            Based on analysis, we see 3 key opportunities:
            1. Operational efficiency through automation
            2. Customer engagement using AI
            3. Data-driven decision making
            
            Let's schedule a call to discuss further.
            
            Best regards,
            AI Solutions Team
            """
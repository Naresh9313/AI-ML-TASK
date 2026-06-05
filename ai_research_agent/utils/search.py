class CompanySearch:
    def __init__(self, tavily_api_key=None):
        self.tavily_api_key = tavily_api_key
    
    def search_company(self, company_name):
        # Simulated search results
        company_lower = company_name.lower()
        
        if "adani" in company_lower:
            return {
                "basic_info": {
                    "what_they_do": "Real estate development arm of Adani Group",
                    "industry": "Real Estate",
                    "scale": "Large enterprise",
                    "geographic_presence": "Major Indian cities",
                    "headquarters": "Ahmedabad"
                },
                "news": [{"title": "New project launches", "summary": "Expanding portfolio"}],
                "competitors": ["DLF", "Godrej"]
            }
        elif "sobha" in company_lower:
            return {
                "basic_info": {
                    "what_they_do": "Real estate developer with backward integration",
                    "industry": "Real Estate",
                    "scale": "Present in 27 cities",
                    "geographic_presence": "South India, Delhi NCR",
                    "headquarters": "Bengaluru"
                },
                "news": [{"title": "Sales growth", "summary": "35% YoY increase"}],
                "competitors": ["DLF", "Prestige"]
            }
        else:
            return {
                "basic_info": {
                    "what_they_do": f"{company_name} operates in their industry",
                    "industry": "Based on business activities",
                    "scale": "Established organization",
                    "geographic_presence": "Key markets",
                    "headquarters": "Business headquarters"
                },
                "news": [{"title": "Growth plans", "summary": "Expanding operations"}],
                "competitors": ["Industry competitors"]
            }
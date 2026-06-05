from typing import Dict, Any

class ReportGenerator:
    def generate_report(self, company_name: str, research_data: Dict, analysis: Dict) -> Dict:
        return {
            "company_overview": research_data.get("basic_info", {}),
            "business_info": {
                "major_offerings": self._get_offerings(company_name),
                "recent_developments": [n.get("title", "") for n in research_data.get("news", [])],
                "expansion_plans": ["Market expansion", "Digital transformation"]
            },
            "challenges": analysis.get("challenges", {}),
            "ai_opportunities": analysis.get("ai_opportunities", {})
        }
    
    def _get_offerings(self, company_name: str) -> list:
        if "realty" in company_name.lower() or "sobha" in company_name.lower():
            return ["Residential Apartments", "Commercial Spaces", "Township Developments"]
        elif "infosys" in company_name.lower():
            return ["Digital Consulting", "Cloud Services", "AI Solutions"]
        else:
            return ["Core Products", "Customer Services", "Digital Solutions"]
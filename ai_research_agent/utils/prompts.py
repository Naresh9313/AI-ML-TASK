def build_analysis_prompt(company_name, basic_info, news_list, competitors_list):
    return f"""
    Analyze {company_name}:
    - What they do: {basic_info.get('what_they_do', 'N/A')}
    - Industry: {basic_info.get('industry', 'N/A')}
    - News: {news_list[:2]}
    - Competitors: {competitors_list[:3]}
    
    Provide specific challenges and AI opportunities for this company.
    """

def build_pitch_prompt(company_name, industry, scale, challenges, opportunities):
    return f"""
    Create a CEO pitch for {company_name} in the {industry} industry.
    Challenges: {challenges}
    Opportunities: {opportunities}
    Make it personal and specific.
    """
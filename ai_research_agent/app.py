import streamlit as st
import os
from dotenv import load_dotenv
from agents.research_agent import ResearchAgent
from agents.llm_factory import LLMFactory
from agents.report_generator import ReportGenerator
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Powered Research & Recommendation Agent")
st.markdown("Enter a company name to generate a complete intelligence report")

# Sidebar for API keys
with st.sidebar:
    st.header("🔑 API Configuration")
    
    # Check if API keys are available
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_gemini = bool(os.getenv("GOOGLE_API_KEY"))
    
    if not has_openai and not has_gemini:
        st.warning("⚠️ No API keys found!")
        openai_key = st.text_input("OpenAI API Key", type="password")
        gemini_key = st.text_input("Gemini API Key", type="password")
        
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
            has_openai = True
        if gemini_key:
            os.environ["GOOGLE_API_KEY"] = gemini_key
            has_gemini = True
    
    # Select provider
    if has_openai or has_gemini:
        options = []
        if has_gemini:
            options.append("Gemini")
        if has_openai:
            options.append("OpenAI")
        
        provider = st.selectbox("Select AI Provider", options)
        
        if provider == "Gemini":
            model = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
        else:
            model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4-turbo-preview"])
        
        depth = st.selectbox("Research Depth", ["Quick", "Standard", "Deep"])

# Main input
company_name = st.text_input("Company Name", placeholder="e.g., Adani Realty, Sobha, Infosys")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚀 Generate Report", type="primary"):
        if company_name:
            with st.spinner(f"Researching {company_name}..."):
                try:
                    # Initialize
                    research_agent = ResearchAgent()
                    llm = LLMFactory(provider=provider.lower(), model_name=model)
                    report_gen = ReportGenerator()
                    
                    # Research
                    st.info("📡 Gathering company data...")
                    research_data = research_agent.research_company(company_name, depth=depth)
                    
                    # Analyze
                    st.info("🧠 Analyzing with AI...")
                    analysis = llm.analyze_company(research_data)
                    
                    # Generate report
                    st.info("📝 Creating report...")
                    report = report_gen.generate_report(company_name, research_data, analysis)
                    
                    # Generate pitch
                    st.info("💼 Writing CEO pitch...")
                    pitch = llm.generate_pitch(company_name, analysis)
                    
                    # Store in session
                    st.session_state.report_data = {
                        "company_name": company_name,
                        "report": report,
                        "analysis": analysis,
                        "pitch": pitch,
                        "provider": provider,
                        "model": model
                    }
                    st.session_state.report_ready = True
                    
                    st.success("✅ Report generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a company name")

# Display report if ready
if st.session_state.get("report_ready"):
    data = st.session_state.report_data
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 Overview", "📊 Business Info", "⚠️ Challenges", 
        "🤖 AI Opportunities", "💼 CEO Pitch"
    ])
    
    with tab1:
        overview = data['report'].get('company_overview', {})
        st.subheader("Company Overview")
        st.write(f"**What they do:** {overview.get('what_they_do', 'N/A')}")
        st.write(f"**Industry:** {overview.get('industry', 'N/A')}")
        st.write(f"**Scale:** {overview.get('scale', 'N/A')}")
        st.write(f"**Geographic Presence:** {overview.get('geographic_presence', 'N/A')}")
    
    with tab2:
        business = data['report'].get('business_info', {})
        st.subheader("Major Offerings")
        for item in business.get('major_offerings', []):
            st.write(f"• {item}")
        
        st.subheader("Recent Developments")
        for item in business.get('recent_developments', []):
            st.write(f"• {item}")
    
    with tab3:
        challenges = data['analysis'].get('challenges', {})
        
        if challenges.get('operational'):
            st.subheader("🔧 Operational Challenges")
            for ch in challenges['operational']:
                st.write(f"• {ch}")
        
        if challenges.get('sales'):
            st.subheader("💰 Sales Challenges")
            for ch in challenges['sales']:
                st.write(f"• {ch}")
        
        if challenges.get('customer'):
            st.subheader("👥 Customer Challenges")
            for ch in challenges['customer']:
                st.write(f"• {ch}")
        
        st.info(f"**Reasoning:** {challenges.get('reasoning', 'Based on analysis')}")
    
    with tab4:
        opportunities = data['analysis'].get('ai_opportunities', {})
        
        for key, value in opportunities.items():
            if value:
                st.subheader(f"📌 {key.replace('_', ' ').title()}")
                for opp in value:
                    st.write(f"• {opp}")
    
    with tab5:
        st.markdown(f'<div style="background: linear-gradient(135deg, #1E88E5, #764ba2); padding: 2rem; border-radius: 15px; color: white;">{data["pitch"]}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Powered by AI | Enter any company name to get started")
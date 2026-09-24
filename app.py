import streamlit as st
from Token_Analysis import get_information
from prompt_compression import PromptCompressionModule
from semantic_compression import SemanticCompressionModule
from prompt_analysis import PromptQualityAnalysisModule


MY_API_KEY = " "

rule_compressor = PromptCompressionModule()
semantic_compressor = SemanticCompressionModule(api_key=MY_API_KEY)
analyzer = PromptQualityAnalysisModule(api_key=MY_API_KEY)

st.set_page_config(layout="wide")
st.title("🚀 AI TOKEN OPTIMIZER & COMPRESSION SUITE")
st.markdown("---")

prompt_input = st.text_area("Type your original prompt here:", height=200)

if st.button("Optimize and Analyze"):
    if prompt_input.strip():
        st.subheader("📊 Original Prompt Metrics")
        stats = get_information(prompt_input)
        st.code(stats)
        st.markdown("---")

        st.subheader("⚙️ Compressed Variations")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Rule-Based Compression")
            rule_out = rule_compressor.compress(prompt_input)
            st.text_area("Result (Rule-Based):", value=rule_out, height=150, key="rule_box")
            st.code(get_information(rule_out))

        with col2:
            st.markdown("### Semantic/AI Compression")
            semantic_out = semantic_compressor.compress(prompt_input)
            st.text_area("Result (AI-Based):", value=semantic_out, height=150, key="semantic_box")
            st.code(get_information(semantic_out))

        st.markdown("---")

        st.subheader("🧠 Prompt Quality Evaluation")
        with st.spinner("Analyzing prompt dimensions..."):
            report = analyzer.analyze_quality(prompt_input)

        if "error" not in report:
            m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
            metrics = ["clarity", "relevance", "specificity", "structure", "redundancy"]
            cols = [m_col1, m_col2, m_col3, m_col4, m_col5]

            for metric, col in zip(metrics, cols):
                with col:
                    score = report.get(metric, {}).get("score", 0)
                    justification = report.get(metric, {}).get("justification", "")
                    st.metric(label=metric.title(), value=f"{score}/5")
                    st.caption(justification)

            st.markdown("#### 💡 Structural Advice")
            st.info(f"**Overall Feedback:** {report.get('overall_feedback', '')}")
            st.success(f"**Suggested Fix:** {report.get('suggested_fix', '')}")
        else:
            st.error(report["error"])
    else:
        st.warning("Please type a valid prompt before processing.")

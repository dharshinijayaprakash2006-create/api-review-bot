import streamlit as st
import requests

st.set_page_config(page_title="API Review Bot", page_icon="🤖")

st.title("🤖 API Review Bot")
st.subheader("Upload your FastAPI code and get instant review!")

file = st.file_uploader("Upload your Python file (.py)", type=["py"])

if file:
    st.success(f" File uploaded: {file.name}")

    code_content = file.read().decode("utf-8")
    st.subheader("📄 Code Preview:")
    st.code(code_content[:300], language="python")

    file.seek(0)

    # Review button
    if st.button("🔍 Review Code"):
        with st.spinner("Analyzing your code..."):
            try:
                file.seek(0)
                response = requests.post(
                    "http://localhost:8000/review/",
                    files={"file": (file.name, file, "text/plain")}
                )
                result = response.json()

                st.subheader("📊 Score:")
                st.metric(label="Code Quality Score", value=result["score"])

                st.subheader("✅ Passed Checks:")
                for item in result["passed"]:
                    st.success(item)

                st.subheader("❌ Issues Found:")
                if result["issues"]:
                    for item in result["issues"]:
                        st.warning(item)
                else:
                    st.info("No issues found!")

                st.subheader("💡 Suggestions:")
                for s in result["suggestions"]:
                    st.info(s)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Download Report button
    if st.button("📥 Download Report"):
        with st.spinner("Generating report..."):
            try:
                file.seek(0)
                response = requests.post(
                    "http://localhost:8000/report/",
                    files={"file": (file.name, file, "text/plain")}
                )
                result = response.json()

                if "report" in result:
                    st.download_button(
                        label="💾 Click here to Save Report",
                        data=result["report"],
                        file_name="review_report.txt",
                        mime="text/plain"
                    )
                    st.success("✅ Report ready — click Save Report!")
                else:
                    st.error("Failed to generate report")

            except Exception as e:
                st.error(f"Error: {str(e)}")
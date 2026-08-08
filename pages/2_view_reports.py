import os
import streamlit as st

st.set_page_config(
    page_title="View Reports",
    page_icon="📊",
    layout="wide",
)

st.title("📊 View Reports")

st.write(
    "View and download your generated interview reports."
)

st.markdown("---")

reports_folder = "reports"

if not os.path.exists(reports_folder):
    st.info("📂 No reports available yet.")

else:
    reports = os.listdir(reports_folder)

    if not reports:
        st.info("📂 No reports available yet.")

    else:
        st.subheader("📄 Available Reports")

        for report in reports:

            report_path = os.path.join(
                reports_folder,
                report
            )

            if os.path.isfile(report_path):

                st.write(f"📄 {report}")

                if report.lower().endswith(".pdf"):

                    with open(
                        report_path,
                        "rb"
                    ) as file:

                        st.download_button(
                            "⬇️ Download PDF",
                            data=file.read(),
                            file_name=report,
                            mime="application/pdf",
                            key=f"download_{report}",
                            use_container_width=True,
                        )

                elif report.lower().endswith(".txt"):

                    with open(
                        report_path,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        content = file.read()

                    with st.expander(
                        f"📋 View {report}"
                    ):

                        st.text(content)

st.markdown("---")

st.caption(
    "🎯 AI Interview Performance Analyzer | Reports"
)
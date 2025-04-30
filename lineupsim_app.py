import streamlit as st
import pandas as pd
import io
from LineupSim_on_Season_Avgs import run_simulation_from_df

st.set_page_config(page_title="Baseball Lineup Simulator", layout="wide")

st.title("⚾ Baseball Lineup Simulator")
st.write("Upload an Excel file with season averages, and simulate thousands of games to see performance insights.")

# === File Upload ===
uploaded_file = st.file_uploader("Upload your Input File (Excel)", type="xlsx")

if uploaded_file:
    try:
        df_input = pd.read_excel(uploaded_file, sheet_name="Input")
        st.subheader("📋 Player Input Data")
        st.dataframe(df_input.head())

        if st.button("Run Simulation"):
            with st.spinner("Simulating 1,000 games..."):
                df_results, df_averages, df_log = run_simulation_from_df(df_input)
            st.success("Simulation Complete!")

            # === Display Results ===
            st.subheader("📊 Average Runs per Inning")
            st.dataframe(df_averages)

            st.subheader("📋 Sample Game Results")
            st.dataframe(df_results.head(10))

            st.subheader("📄 Sample At-Bat Log")
            st.dataframe(df_log.head(10))

            # === CSV Downloads ===
            st.subheader("📥 Download Results (CSV)")

            csv_results = df_results.to_csv(index=False).encode('utf-8')
            csv_averages = df_averages.to_csv(index=False).encode('utf-8')
            csv_log = df_log.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download Game Results (CSV)",
                data=csv_results,
                file_name="game_results.csv",
                mime="text/csv"
            )

            st.download_button(
                label="Download Average Runs per Inning (CSV)",
                data=csv_averages,
                file_name="average_runs.csv",
                mime="text/csv"
            )

            st.download_button(
                label="Download At-Bat Log (CSV)",
                data=csv_log,
                file_name="at_bat_log.csv",
                mime="text/csv"
            )

            # === Excel Download ===
            st.subheader("📥 Download All Results (Excel)")

            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                df_results.to_excel(writer, sheet_name="Game Results", index=False)
                df_averages.to_excel(writer, sheet_name="Averages", index=False)
                df_log.to_excel(writer, sheet_name="At-Bat Log", index=False)

            st.download_button(
                label="Download All Results (Excel)",
                data=excel_buffer.getvalue(),
                file_name="simulation_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")

import pdfx
import json
import pandas as pd
def generate_report(df):  # df: pd.Data
    with pdfx.PDFXCanvas() as pdf:
        pdf.add_page()
        pdf.set_font("Helvetica", 14)
        pdf.write("ML Trading Report\n\n")
        pdf.set_font("Helvetica", 12)
        for i,Én enum(df.items):
            pdf.write(f"\norder: {j\".join(" -")}")
        path = "compliance/report_daily.pdf"
        sd.jseon.dump_report(df, path)
        return path
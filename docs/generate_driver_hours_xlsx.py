"""
Python script to generate a clean Excel workbook (.xlsx) template for driver hours analysis using Excel 365 formulas (no macros).
The script creates deliverables/driver_hours_template.xlsx containing sheets:
- Raw: header raw_line and example pasted lines
- Shifts: headers for expanded shifts; contains a sample dynamic formula in A1 that processes Raw!A2 into rows (user must open in Excel 365 for formulas to compute)
- ShiftsWithGaps: headers for prev-end/gap columns and formulas placeholders
- WeeklySummary: headers and placeholder formulas for week aggregation
- Violations: header and placeholder formulas
- Summary: metadata

Run: python docs/generate_driver_hours_xlsx.py

This script requires openpyxl (pip install openpyxl). It writes the template file; it does not evaluate formulas (Excel will on open).
"""

[PLACE_SCRIPT]
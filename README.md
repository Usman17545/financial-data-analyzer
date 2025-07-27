# 📊 Financial Data Analyzer

A Python-based application that processes and analyzes financial datasets from Excel files.  
It extracts metadata, normalizes formats (currencies, dates), identifies column types, and provides structured access to clean data for further financial modeling or reporting.

---

## 🚀 Features

- ✅ Load multiple Excel sheets
- 🔍 Parse and normalize:
  - Currency formats (`$, €, PKR, etc.`)
  - Date formats (`dd-mm-yyyy`, `Quarterly`, Excel serials)
  - Negative values in brackets, commas, abbreviations (`K`, `M`)
- 📁 Extract metadata:
  - Number of rows and columns
  - Null value counts
  - Column names
- 🧠 Auto-detect column data types:
  - Predicts whether a column is `numeric`, `string`, or `date` based on value percentages
- 📊 Store, aggregate and visualize data
- ⚡ Performance benchmarking for parsing logic

---

## 🛠️ Project Structure


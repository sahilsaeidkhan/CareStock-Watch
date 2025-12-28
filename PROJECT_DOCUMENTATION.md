# CareStock Watch - Hospital Inventory Management System

# CareStock Watch – AI-Powered Inventory Intelligence System

**Author:** Sahil Saeid Khan  
**Last Updated:** 2025  

---

## 1. Project Overview

CareStock Watch is a **Snowflake-native inventory intelligence system** designed for hospitals, public distribution systems (PDS), and NGOs to **predict stock-outs before they happen**, reduce medicine wastage, and support data-driven procurement decisions.

The system runs **entirely inside Snowflake** using Streamlit-in-Snowflake, SQL-based analytics, and AI-ready forecasting logic, ensuring **security, scalability, and zero data movement**.

---

## 2. Problem Addressed

Healthcare and aid organizations often face:
- Late detection of stock-outs
- Overstocking leading to expiry and waste
- Inventory data spread across spreadsheets
- No predictive visibility into future demand
- Poor coordination between procurement and field teams

CareStock Watch converts simple daily stock data into **early warnings, forecasts, and actionable insights**.

---

## 3. Core Features

### 3.1 Inventory Intelligence
- Single live view of inventory health across all locations
- Days-to-stock-out calculation
- Safety buffer analysis
- RED / YELLOW / GREEN risk classification
- Overstock detection to prevent expiry

### 3.2 AI-Assisted Demand Forecasting
- Short-term demand forecasting (7-day horizon)
- Confidence bounds (low / high estimates)
- Explainable, SQL-based logic
- Cortex-ready architecture for future ML model upgrades

### 3.3 Early Warnings & Prioritization
- Critical and warning item identification
- Life-saving item prioritization
- Reorder priority lists per location and item
- CSV export for procurement and field teams

### 3.4 Analytics & Visualization
- Stock health distribution analytics
- Location-wise risk comparison
- Heatmap of locations vs items
- Trend-based operational insights

### 3.5 Human-in-the-Loop Actions
- Action logging for critical items
- Tracks who took action, when, and why
- Supports accountability and audit trails

### 3.6 Impact Measurement
- Estimated patients protected
- Emergency procurement cost savings
- Reduction in medicine wastage
- System coverage (locations × items)

---

## 4. System Architecture (Logical)

**Data Sources**
- Hospitals
- NGOs / Field Centers
- Public Distribution Systems
- Simple daily stock table:
  `(date, location, item, opening_stock, received, issued, closing_stock, lead_time_days)`

**Snowflake Platform**
- Snowflake Tables – Central inventory repository
- Dynamic Tables – Auto-refresh stock health metrics
- SQL Views – Transparent business logic
- Snowpark (Python) – Secure execution inside Snowflake
- Cortex-ready forecasting logic

**Application Layer**
- Streamlit in Snowflake
- No external backend
- No data movement outside Snowflake

**Security & Governance**
- Role-Based Access Control (RBAC)
- Audit-ready design
- Secure-by-default architecture

---

## 5. Technology Stack

### Frontend & Visualization
- Streamlit (inside Snowflake)
- Custom HTML / CSS styling

### Data Platform
- Snowflake
- Dynamic Tables
- SQL Views

### AI & Analytics
- Snowflake Cortex (AI-ready design)
- SQL-based forecasting & stock logic
- Confidence band estimation

### Application Logic
- Python
- Snowpark

### Security & Governance
- Snowflake RBAC
- No external data transfer

---

## 6. Project Structure

# CareStock Watch – AI-Powered Inventory Intelligence System

**Author:** Sahil Saeid Khan  
**Last Updated:** 2025  

---

## 1. Project Overview

CareStock Watch is a **Snowflake-native inventory intelligence system** designed for hospitals, public distribution systems (PDS), and NGOs to **predict stock-outs before they happen**, reduce medicine wastage, and support data-driven procurement decisions.

The system runs **entirely inside Snowflake** using Streamlit-in-Snowflake, SQL-based analytics, and AI-ready forecasting logic, ensuring **security, scalability, and zero data movement**.

---

## 2. Problem Addressed

Healthcare and aid organizations often face:
- Late detection of stock-outs
- Overstocking leading to expiry and waste
- Inventory data spread across spreadsheets
- No predictive visibility into future demand
- Poor coordination between procurement and field teams

CareStock Watch converts simple daily stock data into **early warnings, forecasts, and actionable insights**.

---

## 3. Core Features

### 3.1 Inventory Intelligence
- Single live view of inventory health across all locations
- Days-to-stock-out calculation
- Safety buffer analysis
- RED / YELLOW / GREEN risk classification
- Overstock detection to prevent expiry

### 3.2 AI-Assisted Demand Forecasting
- Short-term demand forecasting (7-day horizon)
- Confidence bounds (low / high estimates)
- Explainable, SQL-based logic
- Cortex-ready architecture for future ML model upgrades

### 3.3 Early Warnings & Prioritization
- Critical and warning item identification
- Life-saving item prioritization
- Reorder priority lists per location and item
- CSV export for procurement and field teams

### 3.4 Analytics & Visualization
- Stock health distribution analytics
- Location-wise risk comparison
- Heatmap of locations vs items
- Trend-based operational insights

### 3.5 Human-in-the-Loop Actions
- Action logging for critical items
- Tracks who took action, when, and why
- Supports accountability and audit trails

### 3.6 Impact Measurement
- Estimated patients protected
- Emergency procurement cost savings
- Reduction in medicine wastage
- System coverage (locations × items)

---

## 4. System Architecture (Logical)

**Data Sources**
- Hospitals
- NGOs / Field Centers
- Public Distribution Systems
- Simple daily stock table:
  `(date, location, item, opening_stock, received, issued, closing_stock, lead_time_days)`

**Snowflake Platform**
- Snowflake Tables – Central inventory repository
- Dynamic Tables – Auto-refresh stock health metrics
- SQL Views – Transparent business logic
- Snowpark (Python) – Secure execution inside Snowflake
- Cortex-ready forecasting logic

**Application Layer**
- Streamlit in Snowflake
- No external backend
- No data movement outside Snowflake

**Security & Governance**
- Role-Based Access Control (RBAC)
- Audit-ready design
- Secure-by-default architecture

---

## 5. Technology Stack

### Frontend & Visualization
- Streamlit (inside Snowflake)
- Custom HTML / CSS styling

### Data Platform
- Snowflake
- Dynamic Tables
- SQL Views

### AI & Analytics
- Snowflake Cortex (AI-ready design)
- SQL-based forecasting & stock logic
- Confidence band estimation

### Application Logic
- Python
- Snowpark

### Security & Governance
- Snowflake RBAC
- No external data transfer

---

## 6. Project Structure
CareStock-Watch/
├── streamlit_app.py
├── requirements.txt
├── .gitignore
├── README.md
├── PROJECT_DOCUMENTATION.md
├── SETUP_GUIDE.md
└── CODE_STRUCTURE.md
## 7. Installation & Setup

### Requirements
- Python ≥ 3.8
- Snowflake account with Streamlit enabled
- Required Python packages (see `requirements.txt`)

### Setup Steps
1. Clone the repository
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
Configure Snowflake connection

Run the app inside Snowflake Streamlit environment

8. Usage Guide
Navigation
Dashboard: Real-time inventory health overview

Analytics: Risk distribution, heatmaps, trends

Actions: Log actions taken on critical items

Impact: Quantified real-world impact

Settings: Alert and notification preferences

Filtering
Filter by location and item

Focus on critical or warning inventory

Export priority lists as CSV

9. Future Enhancements
Automated alert delivery using Snowflake Tasks

EOQ and safety stock optimization

Supplier performance analytics

Expiry-aware forecasting

Multi-warehouse optimization

Role-based dashboards per user type

10. Version History
v1.0

Snowflake-native inventory intelligence

AI-assisted forecasting

Early-warning system

Action logging & impact metrics

11. License
MIT License
(For educational and hackathon purposes)

12. Author
Developed by Sahil Saeid Khan

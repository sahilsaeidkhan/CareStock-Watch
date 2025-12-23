# CareStock Watch - Hospital Inventory Management System

## Project Overview
CareStock Watch is a comprehensive hospital inventory management system built with Streamlit and Snowflake. It provides real-time monitoring and intelligent alerts for hospital medical supplies and medications.

## Features

### Smart Alert System
- **Low Stock Notifications**: Configurable percentage-based alerts when inventory falls below thresholds
- **Expiry Date Alerts**: Automatic notifications for perishable items approaching expiration
- **Overstock Warnings**: Alerts when inventory exceeds optimal levels
- **Alert History**: Complete tracking with severity-based filtering (Critical, High, Medium)
- **Real-time Metrics**: Live dashboard showing total alerts, critical items, and inventory status

### Dashboard
- **Key Metrics**: Total items, low stock count, expiring soon indicators
- **Visual Analytics**: Charts and graphs for inventory trends
- **Status Overview**: Quick view of hospital inventory health

### Inventory Management
- Complete inventory tracking system
- Item categorization and organization
- Historical data and audit logs

### Settings
- Notification preferences (Email, SMS)
- Customizable alert thresholds
- User-configurable options

## Installation

### Requirements
- Python >= 3.8
- Snowflake Account with Streamlit integration
- Required packages (see requirements.txt)

### Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Snowflake connection
4. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Project Structure
```
CareStock-Watch/
├── streamlit_app.py          # Main application file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── PROJECT_DOCUMENTATION.md # This file
└── README.md                # Repository readme
```

## Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: Snowflake
- **Data Processing**: Pandas, NumPy
- **Timezone Handling**: Pytz

## Configuration

### Environment Variables
Set up the following for your Snowflake connection:
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`

## Usage

### Navigation
Use the sidebar to navigate between different sections:
- **Dashboard**: Overview of inventory status
- **Inventory**: Detailed inventory management
- **Smart Alerts**: View and filter active alerts
- **Settings**: Configure preferences

### Filtering Alerts
On the Smart Alerts page:
1. Select severity levels (Critical, High, Medium, Low)
2. Choose alert types (Low Stock, Expiry Alert, Overstock)
3. View filtered results in the data table

## Contributing
To contribute to this project:
1. Create a feature branch
2. Commit your changes
3. Push to the repository
4. Create a Pull Request

## Support
For issues or questions, please create an issue on GitHub or contact the development team.

## Version History
- **v1.0**: Initial release with Smart Alert System
  - Core inventory management
  - Alert system with severity levels
  - Dashboard and analytics

## License
MIT License - See LICENSE file for details

## Author
Developed by Sahil Saeid Khan

---
*Last Updated: 2025*
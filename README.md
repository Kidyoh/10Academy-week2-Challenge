# TellCo Telecom Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tellco-10x.streamlit.app/)

## Project Overview
This project analyzes user behavior data from TellCo, a mobile service provider, to provide insights for potential business acquisition. The analysis combines user engagement metrics, experience indicators, and satisfaction scores to create a comprehensive view of TellCo's service quality and user base.

## Interactive Dashboard
The project includes an interactive dashboard built with Streamlit, providing real-time analysis and visualizations. You can access the dashboard here: [TellCo Analytics Dashboard](YOUR_DASHBOARD_LINK_HERE)

### Dashboard Features
1. **User Overview** (📈)
   - Top handset types and manufacturers
   - Application usage patterns
   - Session duration analysis
   - Principal Component Analysis of user behavior
   - Interactive filters for detailed exploration

2. **User Engagement** (👥)
   - Session frequency metrics
   - Data consumption patterns
   - Top users by various metrics
   - Engagement score distribution
   - Correlation analysis of engagement metrics

3. **User Experience** (🌟)
   - TCP retransmission analysis
   - Round Trip Time (RTT) metrics
   - Throughput analysis by handset
   - Experience score calculation
   - Network performance indicators

4. **User Satisfaction** (😊)
   - Combined satisfaction metrics
   - Engagement-Experience correlation
   - User segmentation matrix
   - Satisfaction score trends
   - Detailed user segments analysis

## Analysis Tasks

### Task 1: User Overview Analysis
- Comprehensive analysis of user demographics
- Handset analysis (top handsets and manufacturers)
- Data usage patterns and trends
- Application usage breakdown
- Key metrics visualization and statistical analysis

### Task 2: User Engagement Analysis
- Session duration patterns and anomalies
- Data volume consumption analysis
- User engagement scoring methodology
- Engagement patterns and trends
- Application usage correlation analysis

### Task 3: User Experience Analysis
- TCP retransmission patterns and impact
- RTT (Round Trip Time) analysis by handset
- Throughput analysis and bottlenecks
- Network performance metrics evaluation
- Experience score calculation and distribution

### Task 4: User Satisfaction Analysis
- Satisfaction score calculation methodology
- User segmentation based on behavior
- Top satisfied customers identification
- Satisfaction prediction modeling
- Engagement-Experience correlation analysis

## Project Structure
```
📦 TellCo-Analytics
 ┣ 📂 data
 ┃ ┣ 📂 raw
 ┃ ┗ 📂 processed
 ┣ 📂 notebooks
 ┃ ┣ 📜 1_user_overview_analysis.ipynb
 ┃ ┣ 📜 2_user_engagement_analysis.ipynb
 ┃ ┣ 📜 3_user_experience_analysis.ipynb
 ┃ ┗ 📜 4_user_satisfaction_analysis.ipynb
 ┣ 📂 src
 ┃ ┣ 📂 analysis
 ┃ ┃ ┣ 📜 user_behavior.py
 ┃ ┃ ┣ 📜 engagement_analyzer.py
 ┃ ┃ ┣ 📜 experience_analyzer.py
 ┃ ┃ ┗ 📜 satisfaction_analyzer.py
 ┃ ┣ 📂 dashboard
 ┃ ┃ ┣ 📂 pages
 ┃ ┃ ┃ ┣ 📜 1_📈_User_Overview.py
 ┃ ┃ ┃ ┣ 📜 2_👥_User_Engagement.py
 ┃ ┃ ┃ ┣ 📜 3_🌟_User_Experience.py
 ┃ ┃ ┃ ┗ 📜 4_😊_User_Satisfaction.py
 ┃ ┃ ┗ 📜 Home.py
 ┃ ┗ 📂 utils
 ┃   ┣ 📜 data_loader.py
 ┃   ┗ 📜 preprocessing.py
 ┗ 📜 requirements.txt
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/Kidyoh/10Academy-week2-Challenge
cd 10Academy-week2-Challenge
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the dashboard:
```bash
streamlit run src/dashboard/Home.py
```

## Technologies Used
- **Python**: Primary programming language
- **Pandas & NumPy**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Streamlit**: Dashboard development
- **Scikit-learn**: Machine learning and statistical analysis

## Data Sources
The analysis uses TellCo's telecommunications dataset, which includes:
- User engagement metrics
- Network performance data
- Device information
- Application usage statistics

## Key Findings
1. **User Behavior**
   - Most popular handset manufacturers
   - Peak usage patterns
   - Application preferences

2. **Network Performance**
   - Average TCP retransmission rates
   - RTT patterns by handset type
   - Throughput bottlenecks

3. **User Satisfaction**
   - Key satisfaction drivers
   - User segment characteristics
   - Areas for improvement

## Future Improvements
- Real-time data integration
- Advanced predictive analytics
- More granular user segmentation
- Additional visualization options
- Performance optimization

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any queries regarding this project, please contact:
- Your Name
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)

## Acknowledgments
- TellCo for providing the dataset
- 10Academy for project guidance
- All contributors and reviewers 
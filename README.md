# OFI Project

A professional project repository for OFI (Optimized Future Initiatives).

## Project Overview

This repository contains the source code and documentation for the OFI project. It's designed to provide a robust and efficient solution for [brief description of what the project does].

## Features

- 1 Interactive Data Visualization - Using Streamlit for dynamic and interactive data exploration
- 2 Logistics Analytics - Tools for analyzing delivery performance and route optimization
- 3 Data Management - Comprehensive data handling with multiple CSV data sources
- 4 Modular Design - Well-structured codebase with separate utility functions
- 5 Configurable Settings - Easy configuration through config.py for different deployment scenarios

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/zaid0602/ofi-project.git
   cd ofi-project
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided in the terminal (usually http://localhost:8501)

3. Use the sidebar to navigate between different sections of the dashboard

## Project Structure

```
windsurf-project/
├── data/                    # Directory for dataset files
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

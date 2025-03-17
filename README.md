# Project Name

## Developer

- **Name:** Isaac Gene Gonzales
- **Email:** isaacgenegonzales@gmail.com

## Repository Overview

This repository contains a Streamlit-based application for data visualization and analysis. The project is structured as follows:

```
project-name/
│── data/                   # Stores raw and processed datasets
│── src/                    # Contains data processing scripts
│── notebooks/              # Jupyter notebooks for EDA
│── streamlit_app/          # Streamlit application code
│── requirements.txt        # Dependencies
│── README.md               # Documentation
│── .gitignore              # Ignored files
```

## Data Download
The data files (both raw and processed) were too large to be included in the repository. Instead, they are hosted on Google Drive. You can download them using the link below:

[Download Data from Google Drive](your-google-drive-link-here)

After downloading:
- Place **raw data** inside the `data/raw/` directory.
- Place **processed data** inside the `data/processed/` directory.

## Running the Streamlit Application Locally

### Prerequisites

Ensure you have Python 3.11 installed.

### Setting Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. To create and activate a virtual environment, run:

```sh
python3.11 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### Installing Dependencies

Once the virtual environment is activated, install the required dependencies:

```sh
pip install -r requirements.txt
```

### Running the App

Navigate to the `streamlit_app` directory and run:

```sh
streamlit run app.py
```

Replace `app.py` with the actual main script of your Streamlit app if different.

The application will be accessible in your browser at `http://localhost:8501/`.

---

For any issues, feel free to contact me!


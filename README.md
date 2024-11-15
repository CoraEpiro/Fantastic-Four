# Team FantasticFour | VGI Challenge - Challenge 3

## Table of Contents
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Project Organization](#project-organization)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Technologies Used](#technologies-used)
- [Usage](#dataset)
    - [Jupyter Notebooks](#jupyter-notebooks)
    - [Web Application](#web-application)
    - [Predicting User Show-Up](#predicting-user-show-up)
- [Analysis Steps](#analysis-steps)
    - [Initial Setup](#initial-setup)
    - [Exploratory Data Analysis and Visualization](#exploratory-data-analysis-and-visualization)
    - [Route and Station Popularity](#route-and-station-popularity)
    - [Demand Analysis](#demand-analysis)
    - [Unused Stops](#unused-stops)
- [Conclusion](#conclusion)
- [Collaborators](#collaborators)

## Introduction
This project analyzes the VGI Flexi bus service data to understand various aspects of the service, such as demand patterns, popular routes, and cancellation reasons. The analysis is performed using Python and Jupyter Notebooks.

## Project Structure

- `main.ipynb`: The main Jupyter Notebook containing the data analysis and visualization.
- `AnalyseDataset.ipynb`: A Jupyter Notebook for initial data exploration and profiling.
- `data/`: Directory containing the input data files (`FLEXI_bus_stops.xls` and `FLEXI_trip_data.xls`).
- `webmap/`: Directory containing the web application for visualizing the data on an interactive map.
- `main.py`: Script containing the model to predict if a user will show up when they call the bus.


## Project Organization

    ├── data                    <- Directory containing the input data files
    ├── DataReports             <- Detailed HTML Reports for the datasets
    ├── heatmaps                <- Heatmaps that show most pickup stations
    ├── webmap                  <- Directory containing the web application for visualizing the data on an interactive map.
    ├── AnalyseDataset.ipynb    <- initial data exploration and profiling
    ├── main.ipynb              <- Notebook containing the data analysis and visualization
    ├── README.md               <- The top-level README for developers using this project.
    ├── requirements.txt        <- Python requirements
    └── VGI_Challenfe.pdf       <- VGI Challenfe PDF

---

## Technologies Used
- **Python** 
- **Pandas**         (Dataframe)
- **Scikit-learn** 
   - **Surprise**    (for collaborative filtering)
- **Matplotlib**     (for data visualization)
- **Seaborn**        (for data visualization)
- **Squarify**       (for data visualization-Tree Map)
- **ydata_profiling**       (for data analyisis)
- **Axios**: A promise-based HTTP client for the browser and Node.js.
- **Bootstrap**: A popular CSS framework for developing responsive and mobile-first websites.
- **Font Awesome**: A toolkit for vector icons and social logos.
- **ShinyApp**: A web framework for developing web applications, originally in R and since 2022 in python.
- **Google Maps API**: Used for showing the map on the web data visualization
- **Folium**: Used to show marks and heatmap on the Map
- **Folium**: Used to show marks and heatmap on the Maps
- **Microsoft Power BI**:  Is an interactive data visualization software product, used to create interactive data charts
- **Dora Web Builder**: Used to create the presentation website


## Setup Instructions

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/Fantastic-Four.git
    cd Fantastic-Four
    ```

2. **Create a virtual environment:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Install additional packages used in the notebooks:**
    ```sh
    pip install numpy matplotlib pandas folium ydata_profiling scikit-learn googlemaps shiny
    ```

## Usage

### Jupyter Notebooks

1. **Run the Jupyter Notebook server:**
    ```sh
    jupyter notebook
    ```

2. **Open `main.ipynb` and `AnalyseDataset.ipynb` in the Jupyter Notebook interface.**

3. **Follow the steps in the notebooks to perform the data analysis and visualization.**

### Web Application

1. **Navigate to the `webmap` directory:**
    ```sh
    cd webmap
    ```

2. **Run the web application:**
    ```sh
    python app.py
    ```

3. **Open your web browser and go to `http://127.0.0.1:8000` to view the interactive map.**

### Predicting User Show-Up

1. **Run the prediction model:**
    ```sh
    python main.py
    ```

2. **The model will predict if a user will show up when they call the bus based on the input data.**

## Analysis Steps

### Initial Setup

- Import necessary libraries and read data from Excel files.
- Merge the trip data with bus stop coordinates for pickups and dropoffs.
- Generate an automatic report about the dataset using the `ydata_profiling` library.

### Exploratory Data Analysis and Visualization

- Determine the number of unique bus stops.
- Analyze the most popular pickup and dropoff stations.
- Visualize the most popular routes by hour.
- Analyze demand patterns by hour.
- Investigate trip status and cancellation reasons.

### Route and Station Popularity

- Identify the most popular pickup and dropoff stations.
- Visualize the most popular routes and their characteristics.

### Demand Analysis

- Analyze hourly demand for the bus service.
- Investigate cancellation patterns and their relation to time and trip characteristics.

### Unused Stops

- Identify bus stops that are not used and investigate potential reasons.

## Conclusion

The analysis provides insights into the VGI Flexi bus service, including demand patterns, popular routes, and cancellation reasons. These insights can help improve the service and address issues such as cancellations and unused stops.

## Collaborators

- [Denis Hoti](https://www.linkedin.com/in/denishoti/)
- [Veronika Rybak](https://www.linkedin.com/in/veronika-rybak-55379a337/)
- [Ali Guliyev](https://www.linkedin.com/in/ali-guliyev-389837238/)
- [Ruslan Tsibirov](https://www.linkedin.com/in/ruslan-tsibirov-6bb6a2262/)
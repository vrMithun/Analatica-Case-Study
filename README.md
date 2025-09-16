# Analytica: Urban Grocers Data Analysis
### *A Project for the Unstop Data Science Competition*

## 1. Project Overview

This project provides an in-depth analysis of the sales data for Urban Grocers Pvt. Ltd. The goal is to evaluate the success of the new management's strategy over two years in the Hyderabad market. By leveraging a comprehensive dataset of daily transactions, this analysis identifies key trends, quantifies the impact of promotions, and provides data-driven recommendations to optimize business operations, improve profitability, and enhance customer satisfaction.

---

## 2. Dataset and Features

The analysis is based on a dataset containing 240,000 transaction-level records from 2023 and 2024.

| Feature           | Description                                     | Data Type    |
|-------------------|-------------------------------------------------|--------------|
| `Date`            | The day of the transaction                      | Date         |
| `Store_ID`        | Supermarket identifier (A, B, C, D)             | Categorical  |
| `Transaction_ID`  | Unique transaction identifier                   | Numeric      |
| `Food_Category`   | Bread, Milk, Fruits, Vegetables, Meat           | Categorical  |
| `Units_Sold`      | Number of units sold in the transaction         | Numeric      |
| `Price_per_Unit`  | Price of a single unit                          | Numeric      |
| `Promotion`       | Binary flag (0 = No, 1 = Yes)                   | Binary       |
| `Holiday_Weekend` | Binary flag (0 = No, 1 = Yes)                   | Binary       |
| `Weather`         | Weather condition (Sunny, Rainy, Cloudy)        | Categorical  |
| `Mode_Purchase`   | Payment method (Cash, UPI, Credit Card, Debit Card) | Categorical  |

---

## 3. Key Questions Addressed

The analysis is structured to answer the core questions posed by the Urban Grocers management team:

* **Peak Sales Periods:** Identification of peak sales days, weeks, and months.
* **Holiday & Weekend Impact:** Quantification of how holidays and weekends affect sales volume across different product categories.
* **Unpredictable Demand:** Identification of the store with the most volatile and unpredictable sales patterns.
* **Promotion Effectiveness:** A quantified analysis of whether promotions successfully increased sales.
* **Demand Patterns & Forecasting:** A detailed look at demand patterns across stores and categories, including a **demand forecast for the next quarter** for a selected category.
* **Investment Analysis:** An evaluation of the initial ₹20 crore investment against the total profit generated, based on a **14% gross profit margin**.

---

## 4. Repository Structure

* `notebooks/`: Contains the Jupyter notebooks used for data cleaning, EDA, analysis, and modeling.
* `data/`: The raw `Urban_Grocers.csv.xlsx` dataset.
* `reports/`: Any generated reports, visualizations, or final presentations.
* `src/`: Scripts for data preprocessing, analysis functions, etc. (if applicable).
* `README.md`: This file.

---

## 5. Getting Started

To run this project locally, follow these steps:

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    ```
2.  Navigate to the project directory:
    ```bash
    cd your-repository-name
    ```
3.  Install the required dependencies (assuming you use `pip`):
    ```bash
    pip install -r requirements.txt
    ```
4.  Launch the Jupyter Notebooks from the `notebooks/` directory to explore the analysis.

---

## 6. Author

**[Your Name]**
* **GitHub:** [Link to your GitHub profile]
* **LinkedIn:** [Link to your LinkedIn profile]

# Car Equity Tracker Utilities

This directory contains utility modules specific to the Car Equity Tracker feature, which provides comprehensive tracking of vehicle finance, costs, depreciation, and equity.

## Modules

### `car_metrics.py`
Core financial calculations and metrics for car equity tracking:
- **Valuation Tracking**: Latest car valuations and mileage tracking with fallback to initial values
- **Finance Calculations**: Outstanding balance, total contributions (deposit + part exchange + payments), interest paid
- **Cost Analysis**: Total cost of ownership, running costs by category, cumulative cost tracking
- **Equity Calculations**: Current equity position, equity percentage, net position vs total contribution
- **PNL Metrics**: Depreciation (purchase price vs current value), cost per mile, total interest paid
- **Cumulative Cost Tracking**: Timeline of all contributions and running costs for charting and analysis

### `car_forecasting.py`
Predictive analytics and forecasting capabilities:
- **Depreciation Forecasting**: Predicts future car values based on historical valuation trends
- **Cost Forecasting**: Estimates future running costs based on historical expense patterns
- **Financial Planning**: Helps with long-term financial planning for vehicle ownership

### `car_data_manager.py`
Data file management and structure:
- **File Generation**: Automatically creates the required Excel file structure with proper sheets and headers
- **Data Validation**: Ensures data integrity and completeness with schema validation
- **Test Data**: Provides sample data for testing and demonstration purposes
- **File Operations**: Handles loading, saving, and updating car data files safely

## Data Structure

The Car Equity Tracker uses a multi-sheet Excel file (`data/car_data.xlsx`) with the following structure:

### Required Sheets

1. **Cars**: Master car details (CarID, Make, Model, PurchasePrice, InitialMileage, etc.)
2. **FinanceAgreements**: Finance contract details (FinanceID, CarID, AmountFinanced, DepositAmount, PartExchangeValue, StartDate, etc.)
3. **FinancePayments**: Payment history (FinanceID, PaymentDate, Amount)
4. **Valuations**: Car value tracking over time (CarID, Date, Value, Mileage)
5. **Expenses**: Running cost log (CarID, Date, Category, Cost, Description)
6. **KeyDates**: Important dates (CarID, Description, ExpiryDate)

### Key Relationships

- Each car has one finance agreement (optional - for cash purchases)
- Finance agreements have multiple payments over time
- Cars have multiple valuations and expenses tracked over time
- Key dates are associated with specific cars (insurance, MOT, etc.)

## Usage

### Basic Setup

```python
from utils.car.car_data_manager import load_car_data, check_and_generate_car_data_file

# Ensure the car data file exists with proper structure
check_and_generate_car_data_file()

# Load all car data
data = load_car_data()
```

### Getting Car Metrics

```python
from utils.car.car_metrics import get_all_car_metrics

# Get comprehensive metrics for a specific car
car_id = 1
metrics = get_all_car_metrics(data, car_id)

# Access specific metrics
equity = metrics['equity']
total_costs = metrics['total_costs']['total_cost']
pnl = metrics['pnl_metrics']['net_position']
cumulative_costs = metrics['cumulative_costs_df']
```

### Key Metrics Available

- **Financial Position**: Current equity, outstanding finance, total contribution
- **Cost Analysis**: Total cost of ownership, running costs by category
- **Performance Metrics**: Depreciation, cost per mile, equity percentage
- **Timeline Data**: Cumulative costs over time for charting and analysis

## Best Practices

### Data Management

- **Regular Updates**: Update valuations and expenses regularly for accurate tracking
- **Categorization**: Use consistent expense categories for better analysis and reporting
- **Validation**: Ensure all required fields are populated for accurate calculations
- **Backup**: Keep regular backups of the car data file

### Performance Considerations

- **Efficient Queries**: Car metrics are calculated on-demand for the selected car only
- **Data Integrity**: Validate data before calculations to prevent errors and ensure accuracy
- **Memory Usage**: Large datasets are processed efficiently with pandas operations

### Integration

- **Card Components**: Use the main card components for displaying car metrics consistently
- **Design System**: Follow the established design patterns for consistent UI across the application
- **Error Handling**: Gracefully handle missing or invalid data with appropriate fallbacks

## Example Workflow

1. **Setup**: Generate the car data file structure using `car_data_manager`
2. **Data Entry**: Populate car details, finance agreements, and initial data
3. **Regular Updates**: Add valuations, expenses, and payments as they occur
4. **Analysis**: Use the dashboard to track equity, costs, and performance over time
5. **Planning**: Use forecasting tools for long-term financial planning and decision making

## Error Handling

The car utilities include comprehensive error handling:

- **Missing Data**: Graceful handling of missing car IDs or incomplete data with appropriate defaults
- **Invalid Calculations**: Protection against division by zero and invalid mathematical operations
- **File Operations**: Safe file creation and loading with fallback options and validation
- **Data Validation**: Checks for required fields and data types to ensure calculation accuracy

## Financial Calculations

### Equity Calculation
```
Current Equity = Latest Valuation - Outstanding Finance
```

### Total Contribution
```
Total Contribution = Deposit + Part Exchange + All Finance Payments
```

### Cost of Ownership
```
Total Cost of Ownership = Total Contribution + Total Running Costs
```

### Net Position (PNL)
```
Net Position = Current Equity - Total Contribution
```

### Cost per Mile
```
Cost per Mile = Total Cost of Ownership / Miles Driven
```

## Future Enhancements

- **API Integration**: Connect to car valuation APIs for automatic updates
- **Advanced Forecasting**: Machine learning models for more accurate predictions
- **Multi-Currency Support**: Support for different currencies and exchange rates
- **Export Features**: Generate reports and export data in various formats (PDF, CSV, etc.)
- **Comparison Tools**: Compare multiple vehicles and their financial performance 
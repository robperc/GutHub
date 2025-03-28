# GutHub

GutHub is a simple recipe search application.

## Prerequisites

- Python 3.x installed
- `pip` (Python package manager) installed
- A virtual environment tool like `venv`

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GutHub
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the development server:
   ```bash
   python -m guthub.app
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Testing the Application

1. Run the test suite:
   ```bash
   python -m unittest tests/backend_tests.py 
   ```

2. Ensure all tests pass successfully.

## Notes

- Make sure to deactivate the virtual environment after use:
  ```bash
  deactivate
  ```

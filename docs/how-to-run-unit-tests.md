# How to run unit tests

Here's a straightforward guide to **running unit tests** for your `md-to-yaml-cli` project.



## ✅ **Step-by-Step Guide**

### 📌 **Step 1: Ensure You're in the Project Directory**

Open your terminal and navigate to the project's root folder (`md-to-yaml-cli`):

```bash
cd path/to/md-to-yaml-cli
```



### 📌 **Step 2: Activate Your Python Environment**

Activate your virtual environment to ensure dependencies are available:

- **On Unix/macOS:**

```bash
source ENV/bin/activate
```

- **On Windows:**

```cmd
ENV\Scripts\activate
```



### 📌 **Step 3: Run All Tests Using pytest**

Run all your unit tests easily with the command:

```bash
pytest
```

This command automatically discovers and runs all tests in your project structure.



### 📌 **Alternative (Manual) Method: Run Individual Test Files**

You can run specific tests individually as well:

**Examples:**

- Parser Tests:
```bash
pytest src/parser/tests/test_markdown_parser.py
```

- Exporter Tests:
```bash
pytest src/exporter/tests/test_yaml_exporter.py
```

- Validator Tests:
```bash
pytest src/utils/tests/test_validator.py
```



## ✅ **Interpreting Test Results**

- **Passing tests** will display a green dot (`.`).
- **Failing tests** will display a red `F`, with details below.
- At the end, pytest provides a concise summary:
  - Number of tests passed or failed.
  - Errors or failures clearly listed.

**Example pytest output:**

```
collected 5 items                                                                                                               

src/exporter/tests/test_yaml_exporter.py .                                                                                [ 20%]
src/parser/tests/test_markdown_parser.py .                                                                                [ 40%]
src/utils/tests/test_validator.py ...                                                                                     [100%]

========================================= 5 passed in 0.17s =========================================
```



## ✅ **Troubleshooting Tips**

- **Module Import Errors?**
  - Ensure `pytest.ini` in your root project directory has:
    ```ini
    [pytest]
    pythonpath = .
    testpaths = src
    ```

- **Test Discovery Issues?**
  - Test file names should follow the format `test_*.py` or `*_test.py`.
  - Test functions should start with `test_`.



## 🚀 **Best Practices**

- Run tests frequently as you add or change functionality.
- Integrate test runs into your Continuous Integration (CI) pipeline for automation.

Using these clear instructions, you can efficiently maintain and verify the integrity of your project through robust testing.
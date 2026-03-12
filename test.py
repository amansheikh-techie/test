import subprocess
import sys
import unittest

import calculator


class CalculatorTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(1, 2), 3)
        self.assertEqual(calculator.add(-1, 5), 4)

    def test_subtract(self):
        self.assertEqual(calculator.subtract(5, 3), 2)
        self.assertEqual(calculator.subtract(0, 5), -5)

    def test_multiply(self):
        self.assertEqual(calculator.multiply(4, 3), 12)
        self.assertEqual(calculator.multiply(-2, 3), -6)

    def test_divide(self):
        self.assertEqual(calculator.divide(10, 2), 5)
        self.assertAlmostEqual(calculator.divide(1, 3), 1/3)
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(1, 0)

    def test_cli_add(self):
        result = subprocess.run([sys.executable, "calculator.py", "add", "3", "4"],
                                capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), "7.0")
        self.assertEqual(result.returncode, 0)

    def test_cli_error(self):
        result = subprocess.run([sys.executable, "calculator.py", "div", "5", "0"],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot divide by zero", result.stderr)



class WebAppTests(unittest.TestCase):
    def setUp(self):
        # import inside to avoid circular import at top-level
        from app import app
        self.client = app.test_client()

    def test_index_page(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Calculator", resp.data)

    def test_calculation_success(self):
        resp = self.client.post("/calculate", data={
            "x": "3",
            "y": "4",
            "operation": "add"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Result: 7.0", resp.data)

    def test_calculation_error(self):
        resp = self.client.post("/calculate", data={
            "x": "5",
            "y": "0",
            "operation": "div"
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b"Cannot divide by zero", resp.data)


if __name__ == "__main__":
    unittest.main()



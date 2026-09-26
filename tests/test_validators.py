import unittest

from transport.services.validators import (validateCapacity, validateDate, validateDateRange,
                                           validateLicenseNumber, validateName, validatePhone,
                                           validateText, validateVehicleNumber)


class TestValidators(unittest.TestCase):
    def testTextIsTrimmedAndRequired(self):
        self.assertEqual(validateText("  Bus  ", "Type"), "Bus")
        with self.assertRaises(ValueError):
            validateText("   ", "Type")
        with self.assertRaises(ValueError):
            validateText("x" * 101, "Type")

    def testName(self):
        self.assertEqual(validateName("Ravi Kumar"), "Ravi Kumar")
        with self.assertRaises(ValueError):
            validateName("R2D2")

    def testPhone(self):
        self.assertEqual(validatePhone("98765 43210"), "9876543210")
        for value in ["12345", "98765abcde", "98765432101"]:
            with self.assertRaises(ValueError):
                validatePhone(value)

    def testVehicleNumberIsUppercased(self):
        self.assertEqual(validateVehicleNumber("ka01ab1234"), "KA01AB1234")
        with self.assertRaises(ValueError):
            validateVehicleNumber("ab")

    def testLicenseNumber(self):
        self.assertEqual(validateLicenseNumber("dl-1234567"), "DL-1234567")
        with self.assertRaises(ValueError):
            validateLicenseNumber("12")

    def testCapacityBounds(self):
        self.assertEqual(validateCapacity(4), 4)
        for value in [0, -1, 201]:
            with self.assertRaises(ValueError):
                validateCapacity(value)

    def testDate(self):
        self.assertEqual(validateDate("2026-02-28"), "2026-02-28")
        for value in ["2026-02-30", "28-02-2026", "tomorrow"]:
            with self.assertRaises(ValueError):
                validateDate(value)

    def testDateRange(self):
        self.assertEqual(validateDateRange("2026-01-01", "2026-01-31"), ("2026-01-01", "2026-01-31"))
        with self.assertRaises(ValueError):
            validateDateRange("2026-02-01", "2026-01-01")


if __name__ == "__main__":
    unittest.main()

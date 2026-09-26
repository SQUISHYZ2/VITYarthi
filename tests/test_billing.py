import unittest

from transport.services.billing import calculateTotalSum, durationToSeconds, secondsToDuration


class TestBilling(unittest.TestCase):
    def testOneHourCostsHourlyRate(self):
        self.assertEqual(calculateTotalSum("01:00:00"), 500.0)

    def testPartialHourIsProrated(self):
        self.assertEqual(calculateTotalSum("00:30:00"), 250.0)
        self.assertEqual(calculateTotalSum("01:15:30"), 629.17)

    def testCustomRate(self):
        self.assertEqual(calculateTotalSum("02:00:00", 100), 200.0)

    def testLongTripOverOneDay(self):
        self.assertEqual(durationToSeconds("30:00:00"), 108000)

    def testInvalidFormatRaises(self):
        for value in ["1:30", "aa:bb:cc", "", "01:-5:00", "01:60:00", "01:00:60"]:
            with self.assertRaises(ValueError):
                durationToSeconds(value)

    def testZeroDurationRaises(self):
        with self.assertRaises(ValueError):
            calculateTotalSum("00:00:00")

    def testInvalidRateRaises(self):
        with self.assertRaises(ValueError):
            calculateTotalSum("01:00:00", 0)

    def testSecondsToDurationRoundTrip(self):
        self.assertEqual(secondsToDuration(durationToSeconds("12:34:56")), "12:34:56")


if __name__ == "__main__":
    unittest.main()

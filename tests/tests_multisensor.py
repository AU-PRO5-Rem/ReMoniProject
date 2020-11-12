#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Unit Tests for "class_multisensor.py"
"""

import unittest
import json

from remoniproject.zwave.class_multisensor import Multisensor
from remoniproject.zwave.fakes.fake_ozwnetwork import FakeOZWNetwork
from remoniproject.zwave.fakes.fake_gateway import FakeGatewayFS

# Global Arrange
_mock_multisensor = FakeOZWNetwork()
_stub_gateway = FakeGatewayFS()


class MultisensorUnitTest(unittest.TestCase):

    def setUp(self):
        # Common Arrange MultisensorUnitTest
        self._uut = Multisensor(_mock_multisensor, _stub_gateway)

    def test_isAwake_SetToAwake_ReturnsTrue(self):
        # Arrange
        _mock_multisensor.status_is_awake = True

        # Act

        # Assert
        self.assertTrue(self._uut.is_awake())

    def test_isAwake_SetToNotAwake_ReturnsFalse(self):
        # Arrange
        _mock_multisensor.status_is_awake = False

        # Act

        # Assert
        self.assertFalse(self._uut.is_awake())

    def test_getValues_JSONloads_CorrectItems(self):
        # Arrange
        expected_dict = json.loads('''
        {
            "Temperature": 12.34,
            "Luminance": 12.34,
            "Relative Humidity": 12.34,
            "Ultraviolet": 12.34,
            "Timestamp":"2020-11-12 23:25:05.684056"
        }
        ''')
        # Act
        self._uut.get_values()
        cut = json.loads(self._uut.sensor_values)

        # Assert
        # Assert that keys and values are a exact match
        self.assertEqual(cut.items(),
                         expected_dict.items())

    def test_WriteValuesToFile_CallOnce_CalledOnceCorrectValues(self):
        # Arrange
        _stub_gateway.write_values_called = 0
        self._uut.sensor_values = "OK"
        # Act
        self._uut.write_values_to_file()
        # Assert
        self.assertEqual(_stub_gateway.write_values_called, 1)
        self.assertEqual(_stub_gateway.values, "OK")

    def test_ReadConfigurationFromFile_CallOnce_CalledOnce(self):
        # Arrange
        _stub_gateway.read_configurations_called = 0
        # Act
        self._uut.read_configuration_from_file()
        # Assert
        self.assertEqual(_stub_gateway.read_configurations_called, 1)

    def test_newtest(self):
        # Arrange

        # Act

        # Assert
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

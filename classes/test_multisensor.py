#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Unit Tests for "class_multisensor.py"
"""

import unittest

from classes.class_multisensor import Multisensor
from classes.interfaces.interface_sensor import ISensor
from classes.test_fakes.fake_ozwnetwork import fake_ozwnetwork

# Global Arrange
_stub_sensor = ISensor()
_mock_multisensor = fake_ozwnetwork()


class MultisensorUnitTest(unittest.TestCase):

    def setUp(self):
        # Common Arrange MultisensorUnitTest
        node_id = 8
        self._uut = Multisensor(_stub_sensor, _mock_multisensor, node_id)

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

    def test_getValues_getsTemperature_CorrectValue(self):
        # Arrange

        # Act

        # Assert


if __name__ == '__main__':
    unittest.main()

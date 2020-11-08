#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Unit Tests for "class_multisensor.py"
"""

import unittest

from class_multisensor import Multisensor
from abstract_classes import ISensor
from abstract_classes import IOZWNetwork
from fakes import fake_network
# Global Arrange
_stub_sensor = ISensor()
_mock_multisensor = fake_network()


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


if __name__ == '__main__':
    unittest.main()

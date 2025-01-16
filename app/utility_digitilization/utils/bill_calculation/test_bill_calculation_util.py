import unittest
from decimal import Decimal
from .bill_calculation_util import (
    calculate_usage_rm_amount,
    calculate_usage_off_peak_amount_rm,
    calculate_md_amount,
    calculate_icpt_rm,
    calculate_clc_percentage,
    calculate_clc_amount,
    calculate_pf_penalty,
    calculate_kwtbb,
    calculate_days,
    calculate_due_rm,
    calculate_total_due,
    calculate_usage_and_validate, calculate_total_bill
)
import pytest
from typing import Dict, List


class TestBillingCalculations(unittest.TestCase):
    class Rate:
        def __init__(self, min_usage_kwh, max_usage_kwh, rate_sen_per_kwh):
            self.min_usage_kwh = min_usage_kwh
            self.max_usage_kwh = max_usage_kwh
            self.rate_sen_per_kwh = rate_sen_per_kwh

    def test_calculate_usage_amount(self):
        """
        Test the get_rate function.
        :return:
        """
        # Mock rates
        rates: List[Dict[str, int]] = [
            {"min_usage_kwh": 0, "max_usage_kwh": 200, "rate_sen_per_kwh": Decimal("43.5")},  # 0 - 200 kWh
            {"min_usage_kwh": 201, "max_usage_kwh": 0, "rate_sen_per_kwh": Decimal("50.9")},  # 201 - 300 kWh
        ]

        # Test with usage =< 200 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=0), Decimal('0'))  # 0 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=2), Decimal('0.87'))  # 0 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=50), Decimal('21.75'))  # 50 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=150), Decimal('65.25'))  # 150 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=200), Decimal('87.00'))  # 200 kWh

        # Test with usage >= 201 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=201), Decimal('87.51'))  # 201 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=202), Decimal('88.02'))  # 202 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=500), Decimal('239.70'))  # 500 kWh
        self.assertEqual(calculate_usage_rm_amount(rates=rates, usage_kwh=1000), Decimal('494.20'))  # 1000 kWh

        # Test with static rates
        self.assertEqual(
            calculate_usage_rm_amount(usage_kwh=0, kwh_static_rate=Decimal("19.2")),
            Decimal('0.00')
        )
        self.assertEqual(
            calculate_usage_rm_amount(usage_kwh=100, kwh_static_rate=Decimal("19.20")),
            Decimal('19.2')
        )
        self.assertEqual(
            calculate_usage_rm_amount(usage_kwh=500, kwh_static_rate=Decimal("19.20")),
            Decimal('96.00')
        )

        # Negative case
        with pytest.raises(ValueError):
            calculate_usage_rm_amount(rates=rates, usage_kwh=-1)

        # Zero rates: should return 0
        self.assertEqual(calculate_usage_rm_amount(rates=[], usage_kwh=100), Decimal('0.00'))

    def test_calculate_off_peak_amount(self):
        """
        Test the calculate_off_peak_amount function.
        :return:
        """
        self.assertEqual(calculate_usage_off_peak_amount_rm(100, 0.5), Decimal('50.00'))
        self.assertEqual(calculate_usage_off_peak_amount_rm(0, 0.5), Decimal('0.00'))

    def test_calculate_md_amount(self):
        """
        Test the calculate_md_amount function.
        :return:
        """
        md_rate: Decimal = Decimal('30.30')
        self.assertEqual(calculate_md_amount(1, md_rate), Decimal('30.30'))
        self.assertEqual(calculate_md_amount(2, md_rate), Decimal('60.60'))
        self.assertEqual(calculate_md_amount(3, md_rate), Decimal('90.90'))

    def test_calculate_icpt_rm(self):
        """
        Test the calculate_icpt function.
        :return:
        """
        # Test with normal values
        self.assertEqual(calculate_icpt_rm(
            usage=7873,
            usage_off_peak=41,
            icpt_rate=Decimal('3.70')
        ), Decimal('292.82'))

        self.assertEqual(calculate_icpt_rm(
            usage=100,
            usage_off_peak=6,
            icpt_rate=Decimal('3.70')
        ), Decimal('3.92'))

        # Test only with usage only
        self.assertEqual(calculate_icpt_rm(
            usage=0,
            icpt_rate=Decimal('3.70')
        ), Decimal('0.00'))

        self.assertEqual(calculate_icpt_rm(
            usage=248,
            icpt_rate=Decimal('2.000')
        ), Decimal('4.960'))

    def test_calculate_clc_percentage(self):
        """
        Test the calculate_clc_percentage function.
        :return:
        """
        self.assertEqual(calculate_clc_percentage(0.8, 0.05, 0.1), Decimal('0.25'))  # PF between 0.75 and 0.85
        self.assertEqual(calculate_clc_percentage(0.7, 0.05, 0.1), Decimal('0.50'))  # PF below 0.75
        self.assertEqual(calculate_clc_percentage(0.9, 0.05, 0.1), Decimal('0.00'))  # PF above 0.85

    def test_calculate_pf_penalty(self):
        """
        Test the calculate_pf_penalty function.
        :return:
        """
        self.assertEqual(calculate_pf_penalty(0.85, Decimal('100'), 0.2), Decimal('20.00'))  # PF below 0.90
        self.assertEqual(calculate_pf_penalty(0.90, Decimal('100'), 0.2), Decimal('0.00'))  # PF above 0.90

    def test_calculate_kwtbb(self):
        """
        Test the calculate_kwtbb function.
        :return:
        """
        kwtbb_rate: Decimal = Decimal('1.60')
        # convert to percentage
        kwtbb_rate = round(kwtbb_rate / 100, 4)
        self.assertEqual(calculate_kwtbb(
            kwtbb_rate=Decimal('0.016'),
            total_usage_amount=Decimal('3992.56')
            ), Decimal('63.89'))  # Tariff B

    def test_calculate_days(self):
        """
        Test the calculate_days function.
        :return:
        """
        self.assertEqual(calculate_days("2021-01-01", "2021-01-01"), 0)
        self.assertEqual(calculate_days("2021-01-01", "2021-01-02"), 1)
        self.assertEqual(calculate_days("2021-01-01", "2021-01-03"), 2)
        self.assertEqual(calculate_days("2021-01-01", "2021-01-04"), 3)

    def test_due(self):
        """
        Test the due function.
        :return:
        """
        # Basic positive scenario
        self.assertEqual(
            calculate_due_rm(
                usage_amount=3992.56,
                usage_amount_off_peak=11.97,
                md_amount=303.00,
                icpt=292.82,
                clc_amount=20.00,
                pf_penalty=0,
                kwtbb=63.89
            ),
            Decimal('4684.24')
        )

        # Zero values scenario
        self.assertEqual(
            calculate_due_rm(
                usage_amount=0,
                usage_amount_off_peak=0,
                md_amount=0,
                icpt=0,
                clc_amount=100.00,
                pf_penalty=0,
                kwtbb=0
            ),
            Decimal('100.00')
        )

    def test_calculate_total_due(self):
        """
        Test the calculate_total_due function.
        :return:
        """
        # Test with normal values
        result = calculate_total_due(
            late_payment_charge_rm=Decimal('0.51'),
            due=Decimal('4684.24'),
            rounding_rm=Decimal('-0.02'),
        )
        self.assertEqual(result, Decimal('4684.73'))

        # Test with zero values
        result = calculate_total_due(
            due=Decimal('0.00'),
            late_payment_charge_rm=Decimal('0.00'),
            rounding_rm=Decimal('0.00'),
        )
        self.assertEqual(result, Decimal('0.00'))

    def test_calculate_usage_and_validate(self):
        """
        Test the calculate_usage_and_validate function.
        :return:
        """
        self.assertEqual(calculate_usage_and_validate(0, 0), 0)
        self.assertEqual(calculate_usage_and_validate(520003, 519309), 694)
        self.assertEqual(calculate_usage_and_validate(520289, 520003), 286)

    def test_calculate_total_bill(self):
        """
        Test the calculate_total_bill function.
        :return:
        """
        self.assertEqual(
            calculate_total_bill(
                total_due_rm=Decimal('0.00'),
                arrears_rm=Decimal('0.00')
            ),
            Decimal('0.00')
        )
        self.assertEqual(
            calculate_total_bill(
                total_due_rm=Decimal('100.00'),
                arrears_rm=Decimal('20.00')
            ),
            Decimal('120.00')
        )
        self.assertEqual(
            calculate_total_bill(
                total_due_rm=Decimal('168.30'),
                arrears_rm=Decimal('500.70')
            ),
            Decimal('669.00')
        )
        self.assertEqual(
            calculate_total_bill(
                total_due_rm=Decimal('0.00'),
                arrears_rm=Decimal('20.00')
            ),
            Decimal('20.00')
        )


if __name__ == '__main__':
    unittest.main()

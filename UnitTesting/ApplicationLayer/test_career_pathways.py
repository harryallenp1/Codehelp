import os
import unittest
from dash import no_update

from UILayer.DashAppUtilities import Get_Program_Options, Get_NOC_Options
from UnitTesting.ApplicationLayer.CareerPathways_Validation import (
    Validate_Program_Pathways,
    Validate_NOC_History_and_Latest,
)
from UILayer.Pages.careerPathways import (  # adjust file name if needed
    Update_Program_Mapping,
    Update_NOC_History,
)

RESULTS_DIR = "UnitTesting/ApplicationLayer/Results"


class CareerPathwaysTests(unittest.TestCase):

    def test_program_pathways_valid_program(self):
        options = Get_Program_Options()
        self.assertGreater(len(options), 0, "No program options returned")

        program_code = options[0]["value"]
        fig = Validate_Program_Pathways(program_code)

        self.assertIsNotNone(fig)
        self.assertGreaterEqual(len(fig.data), 1)

        expected_file = os.path.join(
            RESULTS_DIR, f"{program_code}_Program_Pathways.html"
        )
        self.assertTrue(os.path.exists(expected_file))

    def test_noc_history_and_latest_valid_noc(self):
        noc_options = Get_NOC_Options()
        self.assertGreater(len(noc_options), 0, "No NOC options returned")

        noc_code = noc_options[0]["value"]
        history_fig, latest_fig = Validate_NOC_History_and_Latest(noc_code)

        self.assertIsNotNone(history_fig)
        self.assertIsNotNone(latest_fig)
        self.assertGreaterEqual(len(history_fig.data), 1)
        self.assertGreaterEqual(len(latest_fig.data), 1)

    def test_update_program_mapping_none_returns_no_update(self):
        result = Update_Program_Mapping(Program=None)
        self.assertIs(result, no_update)

    def test_update_noc_history_none_returns_no_update(self):
        result = Update_NOC_History(NOC_Code=None)
        self.assertEqual(result, (no_update, no_update))


if __name__ == "__main__":
    unittest.main()

"""
By: Abira Demello

This module represents the use case of Career Pathways:
 - Program → Career Pathways map
 - Historical NOC employment in Ontario
 - Latest % change in employment by Economic Region

JIRA Issue: PMP-XX   # put your real issue ID here
"""

import plotly.io as pio
from UILayer.DashAppUtilities import (
    Generate_Program_Pathways,
    Generate_NOC_History_In_Ontario,
    Generate_NOC_Latest_ER_PCT,
)

BASE = "UnitTesting/ApplicationLayer/Results"


def Validate_Program_Pathways(program_code):
    fig = Generate_Program_Pathways(Program=program_code)
    pio.write_html(
        fig,
        f"{BASE}/{program_code}_Program_Pathways.html",
        auto_open=False,
    )
    return fig


def Validate_NOC_History_and_ER(noc_code):
    hist_fig = Generate_NOC_History_In_Ontario(NOC_GroupingID=noc_code)
    er_fig = Generate_NOC_Latest_ER_PCT(NOC_GroupingID=noc_code)

    pio.write_html(
        hist_fig,
        f"{BASE}/{noc_code}_NOC_History.html",
        auto_open=False,
    )
    pio.write_html(
        er_fig,
        f"{BASE}/{noc_code}_NOC_ER_PCT.html",
        auto_open=False,
    )

    return hist_fig, er_fig

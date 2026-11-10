"""
Sports Agency External Data Pipeline Package (`src/sports_agency/data_pipeline`)
Integrates verified datasets from Transfermarkt, Capology, Understat, and FBref.
"""

from sports_agency.data_pipeline.external_data_sync import (
    sync_all_external_verified_data,
    sync_capology_verified_wages,
    sync_transfermarkt_verified_contracts,
    get_understat_real_match_moments,
    compute_fbref_radar_percentiles,
)

__all__ = [
    "sync_all_external_verified_data",
    "sync_capology_verified_wages",
    "sync_transfermarkt_verified_contracts",
    "get_understat_real_match_moments",
    "compute_fbref_radar_percentiles",
]

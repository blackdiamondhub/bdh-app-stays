from bdh_sdk import PluginSpec
from bdh_sdk.plugins import LIFECYCLE_ALWAYS, NETWORK_NONE

# No tiles or pages: the app tells the hub when guests (or the owners) are
# staying, which switches the homepage mode, and provides the lodge card.
spec = PluginSpec(
    id="stays",
    app="stays",
    stay="stays.homepage.current_stay",
    card="stays.card.lodge_card",
    api_version=2,
    # The default entities (see homepage.py and card.py). An entity set on the
    # Settings page outside these globs reads as missing.
    permissions=(
        "ha.read:sensor.bdl_stay_*",
        "ha.read:sensor.bdl_modes_status",
        "ha.read:input_select.bdl_occupancy",
        "ha.read:sensor.hot_tub_current_temperature",
        "ha.read:sensor.main_floor_temperature",
    ),
    # Only talks to the hub's broker.
    network=NETWORK_NONE,
    # The hub asks for the stay on every homepage request with a 3 s deadline,
    # too short to wake a stopped container.
    lifecycle=LIFECYCLE_ALWAYS,
    memory_mb=96,
)
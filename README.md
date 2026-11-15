# bdh-app-stays

Black Diamond Hub app that puts the homepage in **guest mode** while guests are
staying (or **owner mode** during an owner visit), and provides the **lodge
card** at the top of the homepage.

It has no pages or tiles. Its `stay` hook reads the sensor published by the
Stays AppDaemon app (`appdaemon-bdl-stays`): `sensor.bdl_stay_current` is
`none` between stays and the guest's name during one, with `guest`,
`arrival`, `checkout` and `owner` attributes. The hub only gets the name,
times and owner flag; door PINs on the sensor are never passed on, because
the homepage is a kiosk.

If Home Assistant can't be reached, or the sensor is `unknown`/`unavailable`
(e.g. AppDaemon hasn't republished it after an HA restart), the hook raises
and the hub keeps the last known stay until its checkout.

## Lodge card

The `card` hook reads all HA states in one request and shows:

| Lodge state | Title | Detail |
|---|---|---|
| Guest stay | Welcome, *guest* | Checkout *when* |
| Owner visit | Welcome back | Leaving *when* |
| `input_select.bdl_occupancy` = `preheat` | Preheating for *guest* / your visit | Ready *arrival* |
| `away` | Vacation mode | Next: *guest*, *arrival* (or No upcoming stays) |
| otherwise | Lodge empty | same as above |

Readings: **Inside** (average of the rooms matching the room pattern) and
**Hot tub**, in °C. Alerts are the `issues` on `sensor.bdl_modes_status`
(failed steps of the last mode change that are still wrong); they clear once
fixed. Tapping the card opens the vacation mode page.

## Settings

| Setting | Default | |
|---|---|---|
| `BDH_STAYS_ENTITY` | `sensor.bdl_stay_current` | HA entity to read |
| `BDH_STAYS_NEXT_ENTITY` | `sensor.bdl_stay_next` | next stay |
| `BDH_STAYS_MODES_ENTITY` | `sensor.bdl_modes_status` | source of alerts |
| `BDH_STAYS_OCCUPANCY_ENTITY` | `input_select.bdl_occupancy` | home / preheat / away |
| `BDH_STAYS_HOT_TUB_ENTITY` | `sensor.hot_tub_current_temperature` | |
| `BDH_STAYS_INSIDE_ENTITY` | `sensor.main_floor_temperature` | thermostat shown as Inside |
| `BDH_STAYS_CARD_URL` | `vacation_mode` | URL name the card opens |

Settings are set on the hub's Settings page. Home Assistant is read through
the hub's broker; the app has no network access of its own.

## Container (hub API 2)

Since 2.0.0 the app runs in its own container (`api_version=2`,
`network=none`, `lifecycle=always` because the hub asks for the stay on
every homepage request, 96 MB). It may only read the entities matching its
`ha.read` permissions (`sensor.bdl_stay_*` plus the default entities above);
an entity set outside them reads as missing. The card link (`card_url`) is a
hub URL name the container can't resolve, so in a container the card has no
link.

## Install

Install from the hub's app store (catalog id `stays`). Running it in the
hub's own process still works: add the hashed line from the latest release to
the site's `apps.txt`.

## Development

CI runs the tests inside the current BlackDiamondHub `main` using
`bdh-sdk`'s reusable `app-ci.yml`. Bump `version` in `pyproject.toml` and
merge to `main` to publish a release.

# Witty One Integration

> [!WARNING]
> Work in progress, the list of sensor may change and you may need to re-add this integration.


[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
<!-- [![BuyMeCoffee][buymecoffeebadge]][buymecoffee] -->


Integration to integrate with Hager Witty One charging station.

This integration only support Witty One, it do not support other Witty charging station (Witty Start...).


<!-- **This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from blueprint API. -->

## Bluetooth connection

For now, no-one have succeed to connect directly with a bluetooth adapter directly connected to the Home assistant.
We only manage to connect through a BLE Proxy using ESPHome.
If you manage to connect directly let me know.

### Remark on Ble Proxy with ESPHome

This ESP sdk has a limitation for the number of data read in one time from a BLE device, the default value is to small so the configuration
must include the following.

```yml
esp32:
  board: esp32dev
  framework:
    type: esp-idf
    # increase the number of characteristic read by the ESP
    sdkconfig_options:
      CONFIG_BT_GATTC_MAX_CACHE_CHAR: "95"


bluetooth_proxy:
  active: True
```

## Installation


### Manually
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `witty_one`.
1. Download _all_ the files from the `custom_components/witty_one/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. Put the charging station in pairing mode with the card : the led must blink blue.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Witty One Integration"

### With HACS

This integration is not published yet into HACS (need to add icon and finish it a little more). But you can add a custom repository `ngraziano/hass-witty` with the type `integration` and then install `Witty One Integration`

After adding the integration :

1. Restart Home Assistant
1. Put the charging station in pairing mode with the card : the led must blink blue.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Witty One Integration" and add it.


## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[witty_one]: https://github.com/ngraziano/hass-witty
[buymecoffee]: https://www.buymeacoffee.com/ngraziano
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/ngraziano/hass-witty.svg?style=for-the-badge
[commits]: https://github.com/ngraziano/hass-witty/commits/main
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/ngraziano/hass-witty.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Nicolas%20Graziano%20%40ngraziano-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ngraziano/hass-witty.svg?style=for-the-badge
[releases]: https://github.com/ngraziano/hass-witty/releases

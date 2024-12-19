# Witty One Integration

> [!WARNING]
> Work in progress
> Nothing to see now, only a template

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
<!-- [![BuyMeCoffee][buymecoffeebadge]][buymecoffee] -->

<!-- [![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum] -->

_Integration to integrate with [witty_one][witty_one]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from blueprint API.
`switch` | Switch something `True` or `False`.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `witty_one`.
1. Download _all_ the files from the `custom_components/witty_one/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Witty One Integration"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[witty_one]: https://github.com/ngraziano/witty_one
[buymecoffee]: https://www.buymeacoffee.com/ngraziano
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/ngraziano/witty_one.svg?style=for-the-badge
[commits]: https://github.com/ngraziano/witty_one/commits/main
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/ngraziano/witty_one.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Nicolas%20Graziano%20%40ngraziano-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ngraziano/witty_one.svg?style=for-the-badge
[releases]: https://github.com/ngraziano/witty_one/releases

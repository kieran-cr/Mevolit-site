---
outline: deep
---

# Mevolit Use cases

::: warning IMPORTANT NOTE: Update Your Use of Mevolit Feed

**Implement a USER-AGENT in Custom Tools**

To optimize hosting and caching for Mevolit, please implement a user-agent in your integrations, tools, and workflows. This enhances performance and user interactions with Mevolit.

**Mevolit Feed Usage**

Please ensure your scripts that are utilising the Mevolit macOS and iOS feeds to point to https://sofafeed.macadmins.io/v1/macos_data_feed.json and https://sofafeed.macadmins.io/v1/ios_data_feed.json respectively.

:::

## Osquery

Use [Osquery](https://osquery.io) with the MacAdmins Open Source (MAOS) [Osquery Extension](https://github.com/macadmins/osquery-extension) and the new Mevolit tables to monitor unpatched CVEs on macOS. By leveraging the `sofa_unpatched_cves` and `sofa_info` tables, you can identify vulnerabilities and patch levels not addressed by current system updates across your fleet. This use case enhances security monitoring by providing insights into unpatched and actively exploited CVEs, ensuring systems are kept up to date and secure.

For more details, visit the original blog post about Mevolit and MacAdmins Osquery Extension [here](https://grahamgilbert.com/blog/2024/05/03/investigating-unpatched-cves-with-osquery-and-sofa/).

## Nudge 2.0

Nudge is a MacAdmins Open Source tool designed to encourage the installation of macOS security updates. The latest release, Nudge 2.0, integrates with the Mevolit feed to keep macOS systems up to date. By default, it checks the Mevolit feed every 24 hours, caching the data locally. Users can customize the refresh interval, set a custom feed URL, and manage support for unsupported devices. Customizable UI elements indicate when a device is unsupported, with text fields and overlay icons to highlight this status.

For more details, visit the [Nudge Wiki](https://github.com/macadmins/nudge/wiki/v2.0-features).


## Using Mevolit with Jamf Pro

Integrate Mevolit with Jamf Pro to monitor macOS and XProtect updates. Mevolit provides up-to-date information on macOS versions and XProtect updates, allowing you to determine if systems are compliant. Use Jamf Pro Extension Attribute scripts (`macOSVersionCheck-EA.sh` and `XProtectVersionCheck-EA.sh`) to check local system versions against the latest updates in the Mevolit JSON feed. Results can be used to scope non-compliant computers into Smart Groups, triggering MDM/DDM commands to ensure systems are updated.

For more details, visit the original blog posts here:
- [Mevolit, and how to use it with Jamf Pro](https://grahamrpugh.com/2024/04/29/sofa-and-jamf-pro.html)
- [If you're using the Mevolit feed, please take note!](https://grahamrpugh.com/2024/07/22/sofa-new-feed.html)

## More use cases

Check out further use case examples in our documentation.

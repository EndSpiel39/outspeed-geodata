# OutSpeed GeoData

Independent GeoSite database for OutSpeed VPN. Existing Loyalsoldier `geoip.dat` and `geosite.dat` remain unchanged.

## Editing

Edit [domains.txt](domains.txt) on GitHub. Use:
- `domain:animeozi.space` — this domain and **all its subdomains**, including newly created ones.
- `full:host.example.com` — only the exact host.

Every push to `main` that changes the list triggers a build and publishes `outspeed.dat` to the release tagged `latest`.

## Download

https://github.com/EndSpiel39/outspeed-geodata/releases/latest/download/outspeed.dat

## Client Xray configuration (one-time)

Add this independent item to `geodata.assets` while preserving the existing Loyalsoldier entries:

```json
{
  "url": "https://github.com/EndSpiel39/outspeed-geodata/releases/latest/download/outspeed.dat",
  "file": "outspeed.dat"
}
```

Add this rule near the **top** of `routing.rules`, before broader routing rules:

```json
{
  "type": "field",
  "domain": ["ext:outspeed.dat:outspeed-direct"],
  "outboundTag": "direct"
}
```

The `direct` outbound must be present, and the `geodata.cron` schedule controls when the client downloads updates. **The rule must be on the client device** to route user traffic directly rather than through the VPN. Updating a server-side Xray file alone will not change routing on users' devices.

The initial `outspeed.dat` must be downloaded before Xray starts with the new `ext:` rule. Support for scheduled hot reload depends on the client/core integration.

## Privacy

The repository is currently public. If you make the repository private, the unauthenticated release download will stop working. Anyone obtaining `outspeed.dat` may be able to inspect its domain entries.

# SaltyFork landing page

A temporary static introduction while the product is in development. Uses the
existing SaltyFork logo; no account collection or tracking. The product's Next.js
web app and .NET API will be implemented separately.

Build and preview from this directory:

```sh
docker build -t saltyfork-landing:local .
docker run --rm -p 8080:8080 saltyfork-landing:local
```

Open http://localhost:8080. The container runs nginx as an unprivileged user;
`/healthz` is the hosting probe endpoint. Check desktop and mobile layouts and
the navigation/GitHub links before deployment.

The copied files under `public/assets/` come from the repository's `assets/`.
Update both when the brand changes.

The hero uses a cropped, web-sized transparent full-body PNG (1000 pixels tall).
The full-resolution PNG and SVG trace are preserved in `assets/`. The navy header/footer/favicon
uses the existing `logo-mark-square-tight.svg` framing. A full-body SVG trace is
saved in the main assets directory for reference; it is not used in the hero.

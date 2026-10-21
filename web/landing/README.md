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

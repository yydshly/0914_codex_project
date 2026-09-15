# create-vibe-motion-3d

Monorepo for a 3D animation scaffold. It mirrors the `create-vibe-motion` shape, but the generated project uses Three.js for scene rendering and Puppeteer for deterministic frame export instead of Remotion.

## Packages

- `packages/template`: source template used for local development.
- `packages/create-vibe-motion-3d`: npm create package that embeds the template.

## Local Development

```bash
pnpm install
pnpm dev
```

`pnpm dev` starts the template export server and serves the scene at the printed URL.

## Test The CLI Locally

```bash
pnpm sync-template
pnpm create:local /tmp/vibe-motion-3d-test --skip-install
cd /tmp/vibe-motion-3d-test
pnpm install
pnpm dev
```

## Release Flow

1. Edit `packages/template`.
2. Run `pnpm verify`.
3. Run `pnpm sync-template`.
4. Commit the template and CLI package changes.
5. Push a `v*` tag, for example `v1.0.0`, to trigger the npm publishing workflow.

The npm package has a `prepublishOnly` hook that syncs the latest template into the CLI package before publishing. The GitHub Actions workflow publishes `packages/create-vibe-motion-3d` to npm when a version tag is pushed.

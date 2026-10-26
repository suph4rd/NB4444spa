# NB4444 frontend

## Project setup

Use Node.js `^20.19.0` or `>=22.12.0` and install the locked dependencies:

```
npm ci
```

### Development server

```
npm run serve
```

### Production build

```
npm run build
```

The app is built with Vite. Set `VITE_API_PORT` to override the backend port
(defaults to `8008` for local development and `9999` in the production image).

CKEditor 5 defaults to its GPL license key. For a commercially licensed
deployment, provide the appropriate `VITE_CKEDITOR_LICENSE_KEY` at build time.
See the [CKEditor 5 licensing guide](https://ckeditor.com/docs/ckeditor5/latest/getting-started/licensing/license-key-and-activation.html).

Vue CLI configuration has been replaced with [`vite.config.mjs`](./vite.config.mjs);
see the [Vite guide](https://vite.dev/guide/).

### Migration references

- [Vue CLI maintenance status and tooling guidance](https://vuejs.org/guide/scaling-up/tooling#vue-cli)
- [Vue CLI to Vite migration guide](https://vueschool.io/articles/vuejs-tutorials/how-to-migrate-from-vue-cli-to-vite/)
- [Vuetify upgrade guide](https://vuetifyjs.com/getting-started/upgrade-guide/)
- [Vue Router 4 to 5 migration guide](https://router.vuejs.org/guide/migration/v4-to-v5.html)
- [CKEditor 5 predefined-build migration](https://ckeditor.com/docs/ckeditor5/latest/updating/nim-migration/predefined-builds.html)

# playgta5 Source Code
This code is grabbed from playgta5.com before it got took down. You can run this locally or make it public hehe.

# Credits
Shoutout to Sebas Furbastian on Telegram for scrapping this code. Idk what is his GitHub but here's the Telegram and X.

Telegram: @SebasKitten

X: @Sebas_Kitten

# Link
Telegram: https://t.me/playgta5regen


# Disclaimer
I don't host the `.\mirror` folder since it has copyrighted content from Rockstar Games. Please find the files by yourself.

No copyrighted file is included in this repo. If Rockstar Games or any affiliated group think this repo has copyright infringement things, email me at shadany7824@gmail.com for me to took it down.

And don't email me for asking the mirror folder. I will not reply to the email.

# How to use

Install Docker with Docker Compose, then clone this repository.
Place your existing mirror at `.mirror` beside the repository files. The
mirror is not downloaded or included in the image.

Supported layouts are `.mirror/playgta5.com/data/` (the original export) and
`.mirror/data/` (site contents directly). The same site root must contain
`b/8b0b5899ed/game.wasm`, shader packs, audio-worklet.js, title art and the
other exported assets. Files must be readable by the unprivileged container user.

```sh
docker compose up --build -d
```

Open http://localhost:8000/. For a mirror elsewhere, put its location in a
local `.env` file before starting Compose.

```dotenv
MIRROR_PATH=/absolute/path/to/.mirror
```

On Windows with Docker Desktop, use a path like `C:/games/.mirror`.
Missing mount directories fail instead of silently creating an empty mirror.
Stop with `docker compose down`; view logs with `docker compose logs -f`.

# Container details

The builder arranges tracked HTML, JavaScript and manifests at the client URLs.
The Python slim runner preserves the existing server's byte-range support,
binary `POST /data/batch` endpoint (including gzip), correct WASM MIME type
and cross-origin isolation headers. Tracked client files take precedence over
copies in the mirror. The mirror is mounted read-only and excluded from the
build context. The container runs unprivileged with a read-only filesystem.

The bundled Windows runtime, old launchers and offline investigation artifacts
are removed. Data and shader manifests remain because the client loads them.

# Verification

`docker/smoke_test.py` checks a running container using synthetic mirror assets.
Create an otherwise empty fixture directory with `data/smoke.bin` containing
ASCII `0123456789` and `b/8b0b5899ed/game.wasm` containing the eight bytes
`00 61 73 6d 01 00 00 00`. Start Compose with `MIRROR_PATH` set to that directory,
then run `python docker/smoke_test.py`. Tests cover the index, client routes,
isolation headers, MIME, ranges, batch/gzip and traversal rejection.
Synthetic fixtures verify the server, not gameplay.

Actual gameplay requires the complete mirror and a browser supporting WebGPU
and cross-origin-isolated shared memory. Remote browser access also requires
HTTPS; localhost works without it. This is a local server, not a hardened
public hosting service.

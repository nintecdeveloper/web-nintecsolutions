# Publication workflow

This project publishes through GitHub → Vercel. Production remote:
https://github.com/nintecdeveloper/web-nintecsolutions.git
Production branch: main.

Standing user authorization (2026-09-14): always commit and push completed, validated changes to origin/main. Do not wait for a separate publication request. Honor any later explicit local-only instruction. Do not publish broken or unfinished work.

On an authorized publication: inspect changes and remote state, run relevant builds/tests and the secrets check, stage only reviewed files, commit descriptively, push normally to origin/main, and report the full sent commit hash. Verify GitHub/Vercel deployment status when available. Never force push or discard remote work. Reconcile remote changes before pushing. Do not publish through Sites as a substitute for this workflow. Do not change DNS or Wix without explicit authorization.

The remote contains manually uploaded dist files. Preserve them; regenerate the production build before staging dist changes. scripts/build_vercel.py remains Vercel's build command. Never stage nested local clones, environment files, credentials, or private files.

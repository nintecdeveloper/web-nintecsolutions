# Pricing and audit — publication, 2026-10-22

The user explicitly authorized publishing this reviewed pricing/audit revision on 2026-10-22 with “commit push”, superseding the earlier local-only instruction.

## Shared templates and translations

`src/pricing.html` uses the existing build-time CA/ES/EN/NL catalogues. The five included-usage disclosures and sixteen tooltips are rendered in those same languages. `src/pricing.js` only handles help visibility and viewport positioning; no translations or forms are duplicated.

Allowances (phone numbers / monthly AI voice minutes / WhatsApp AI replies / WhatsApp utility messages):

- Starter: 1 / 150 / 600 / 250.
- Basic: 1 / 300 / 1,000 / 500.
- Pro: 2 / 500 / 1,600 / 800.
- Premium: 3 / 1,000 / 3,000 / 1,500.
- Enterprise: custom volumes; no fixed quantities.

No included marketing allowance is displayed. The campaign feature stays in Pro. Starter's WhatsApp allowances follow the supplied table even though its main feature list focuses on voice; no product entitlement configuration is present in this repository to independently validate feature provisioning.

All pricing CTAs open the existing two-step audit modal. Name/email/privacy remain required; company/phone are optional. The automation-task question is removed from the full contact form (it was already absent from the modal). Existing attribution remains in the backend `missatge` column; no customer question is sent.

## Calendar findings and limits

- Source of real busy slots: existing Supabase `rpc/get_franges_ocupades` with date range. The repository has no Google Calendar connector or server schema; any upstream synchronization cannot be independently verified here.
- Existing frontend `dailyBlocks()` was already limited to 2–4 date-seeded slots. It now spreads them between morning and afternoon without adjacent slots. It creates no database records or calendar events.
- Business hours remain 09:00–11:30 and 15:00–16:30, on the same ten 30-minute start times, weekdays, current and following calendar week. Madrid timezone and one-hour notice remain unchanged.
- `blocked`, `reserved` and `restricted` flags distinguish artificial, RPC-returned and notice/past-time restrictions. The displayed `taken` state is their union. Real busy slots are never capped at four or reopened.
- Availability is still rechecked before insertion. HTTP 409 handling is preserved. Atomic protection against simultaneous bookings depends on the existing backend constraint/transaction, which is not in this repository and was not modified.
- Booking payloads, conflicts, failures and optional fields are tested with a local fake transport. UI checks progress to availability but do not confirm a booking or create test leads.

Build/test production output is a local check only. `python3 build.py` restores the noindex local preview. No React/TypeScript migration, backend change, new form or integration was introduced.

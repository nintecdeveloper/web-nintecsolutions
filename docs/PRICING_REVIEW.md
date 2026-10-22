# Pricing — publication and maintenance

The user authorized publication of the reviewed five-plan version on 2026-10-22 with “fes push commit”. The displayed prices and features are the reviewed version. Exact gift-minute quantities have not been supplied and remain hidden; do not invent them.

Preview: `python3 build.py` and serve `dist` on loopback. This build is noindex. The production build used by tests is only a local verification, not deployment.

Shared template: `src/pricing.html`; translations: existing `src/locales/{es,en,nl}.json`. No new translation framework. Pricing navigation follows Nintec360 in each locale.

Gift minutes: each plan has a `.pricing-gift[data-plan]` area and an empty, hidden `[data-gift-minutes]` span. Once amounts are approved, enter the localized amount label in this span, add it to the existing catalogues and remove `hidden`. Never show an unapproved quantity or placeholder. Update the pricing test when approved quantities are introduced.

All page CTAs link to the existing locale-specific `/contacte/` audit page. No checkout, forms, booking logic or integrations were changed.

# Non-electrical fields removed from the IDM

The Interoperability Data Model (IDM) standardizes the electrical specifications of DC power
system components. The schemas were synced from the dcide-app zod validators, which also
carry commercial, catalog and app-internal fields. Those do not belong in the IDM; they stay
in the dcide-app validators. This change removes them from `schema/` and `examples/`.

The removal is applied by `scripts/strip_nonelectrical.py` (re-runnable). Every field below
lives in the shared base that all 31 component schemas inline, unless marked component
specific. After removal all 31 schemas are valid draft-07 and all 31 examples validate, with
no dangling `$ref`.

## Removed and why

Commercial (distributor, pricing, availability):

- `distributors` and `distributorsDetails`: distributor references and per distributor price.
- `msrp`: manufacturer suggested retail price.
- `leadTime`: procurement lead time.
- `regionAvailability`: where the product is sold.

Catalog / marketing:

- `website`: product marketing page URL.
- `questions`: marketing Q and A pairs.
- `images`: product photos (thumbnail, ISO picture, front, rear, and so on).

dcide-app internal (team scoping, UI annotations, derived helpers, system, analytics):

- `teamManufacturer`: team scoped manufacturer reference.
- `metadata`: per field UI display and notes annotations.
- `compatibleWithCrossReference`: derived compatibility cross references.
- `compatibleWithPlaceholders`: unresolved compatibility placeholders.
- `id`: app assigned record id.
- `visibility`, `reviewed`, `publishedBy`, `publishedAt`, `archivedAt`, `deletedAt`: record
  publishing and lifecycle-management flags and timestamps.
- `completeness`, `viewedCount`: app metrics and analytics.

Component specific (dcide-app modeling helpers, also reference removed fields):

- `canServeAs` (breaker, rapidShutdownDevice): referenced `compatibleWithPlaceholders`.
- `compatibleProducts` (combinerBox, powerDistributionUnit): referenced `id`.

## Kept as electrical spec or identification

`type`, `name`, `description`, `manufacturer`, `productIdentifier`, `productSeries`
(identification of the product the specs describe); `application`, `compliance`, `standards`,
`specificationsSummary`; `communication`, `environmental`, `mechanical`, `performance`; and
the whole `electrical` section (ports, voltages, currents, power, ratings, impedances,
capacitances, protection ratings, thermal, and component specific electrical attributes).

## Ambiguous, kept for human review

These could be spec relevant, so they were NOT deleted. Flagged here for a human decision:

- `lifecycle` (`release`, `endOfLife`): product lifecycle dates. Availability adjacent, but
  end of life can matter for system design and long term maintenance planning.
- `files`: references to datasheets and manuals. The document links are spec relevant, though
  the field also models dcide-app file storage (ids, urls). Consider narrowing rather than
  dropping.
- `compatibleWith`: declared compatible components. Compatibility is arguably core to an
  interoperability data model, even though the values are component references.

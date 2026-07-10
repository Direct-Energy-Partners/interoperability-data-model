# Non-electrical fields removed from the IDM

The Interoperability Data Model (IDM) standardizes the electrical specifications of DC power
system components. The schemas were synced from the dcide-app zod validators, which also
carry commercial, catalog and app-internal fields. Those do not belong in the IDM; they stay
in the dcide-app validators. This change removes them from `schema/` and `examples/`.

The removal is applied by `scripts/strip_nonelectrical.py` (re-runnable). Every field below
lives in the shared base that the component schemas inline, unless marked component specific.
After removal all schemas are valid draft-07 and all examples validate, with no dangling
`$ref`. The result keeps only electrical spec, identification and compliance fields.

## Removed component types

Five component types were removed entirely (schema, example and guide page): `grounding`,
`hydro`, `fuelCell`, `wind`, `utility`. The model now covers 26 component types. The removed
`utility` value was also dropped from the port `purpose` enum in `charger`, `combinerBox`,
`converter` and `powerDistributionUnit`, and from their guide pages.

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

Previously flagged as ambiguous, now removed at operator request:

- `lifecycle` (`release`, `endOfLife`): product lifecycle dates. Availability adjacent, not an
  electrical spec.
- `files`: references to datasheets and manuals, plus dcide-app file storage metadata.
- `compatibleWith`: declared compatible component references.

## Kept as electrical spec or identification

`type`, `name`, `description`, `manufacturer`, `productIdentifier`, `productSeries`
(identification of the product the specs describe); `application`, `compliance`, `standards`,
`specificationsSummary`; `communication`, `environmental`, `mechanical`, `performance`; and
the whole `electrical` section (ports, voltages, currents, power, ratings, impedances,
capacitances, protection ratings, thermal, and component specific electrical attributes).

## Ambiguous, kept for human review

None. The three fields previously flagged here (`lifecycle`, `files`, `compatibleWith`) were
removed at operator request; see the removal list above.

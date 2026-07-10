# Diode

A diode conducts current in one direction and blocks it in the reverse direction. In a DC
system it is used for blocking, freewheeling, oring and reverse polarity protection, so power
passes from one terminal to the other only when forward biased.

- Type key: `diode`
- Indicator: `D`
- Plural: Diodes
- Ports: 2, shown as a single port in the diagram. Each port carries both an AC and a DC block.
  Power flow may be input, output or bidirectional.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A diode has exactly two ports, which are displayed as a single port in the diagram. The two
ports share the same definition and are kept in sync. Each port defaults to
`powerFlowDirection` `bidirectional`. On top of the abstract port base (features, terminal,
wire size) each port carries:

- An AC block with `enabled`, `voltage`, `current`, `frequency`, `powerFactor` and
  `configuration`. The standard AC `power` and `earthingConfigurations` fields are omitted for
  this type.
- A DC block with `enabled`, `voltage`, `current` and `configuration`. The standard DC `power`
  and `earthingConfigurations` fields are omitted for this type.

The diode adds no extra port level attributes beyond the abstract base and the reduced AC and
DC blocks.

## Electrical

The `electrical` section holds only the ports.

- `ports` (tuple of 2 ports): see above.

## Example

See [`examples/testDiode.json`](../examples/testDiode.json).

# Power Distribution Unit

A power distribution unit (PDU) is a device fitted with multiple outputs designed to distribute
electric power, especially to racks of computers and networking equipment located within a data
center. In a DC system it takes one or more feeds and splits them across many downstream
outputs. The IDM models a PDU as a variable number of ports, each carrying an AC block, a DC
block, or both.

- Type key: `powerDistributionUnit`
- Indicator: `PDU`
- Plural: Power Distribution Units
- Ports: 2 or more, input, output or bidirectional, AC and DC

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

A power distribution unit has two or more ports (no fixed count, the minimum is 2 and there is
no maximum). By default the first port is an input and the second is an output, and each port
may be set to input, output or bidirectional. Each port carries both an AC block and a DC block
(as described in the shared port model). On top of the abstract port base (features, terminal,
wire size) and the AC and DC blocks, each PDU port adds:

- `description` (string, default empty): free text note about the port.
- `purpose` (enum, nullable, default `null`): the role the port serves, one of `battery`,
  `converter`, `solar`, `utility`, `panel`, `charger`, `generator`.

## Electrical

The `electrical` section holds the ports. In addition, the type carries a top level
`compatibleProducts` key.

- `ports` (array of 2 or more ports): see above.
- `compatibleProducts` (array of component id strings): products known to work with this PDU.
  Defaults to empty.

## Environmental

The power distribution unit uses the standard environmental section as described in
[common attributes](./common.md).

## Example

See [`examples/testPowerDistributionUnit.json`](../examples/testPowerDistributionUnit.json).

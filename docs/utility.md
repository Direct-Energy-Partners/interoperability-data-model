# Utility

A utility represents the connection to the public electricity network, also known as the grid
or the net. It is the point where a microgrid imports and exports power against the wider
system. In the IDM a utility is modelled as a single bidirectional port that defaults to AC,
carrying both an AC and a DC block.

- Type key: `utility`
- Indicator: `GRID`
- Plural: Utilities
- Ports: 1, bidirectional, AC by default (carries both an AC and a DC block)

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A utility has exactly one port. The port is fixed to bidirectional power flow, since the grid
both supplies and absorbs power. The port carries both an AC block (voltage, current, power,
frequency, power factor, configuration, earthing) and a DC block (voltage, current, power,
configuration, earthing) on top of the abstract port base (features, terminal, wire size). The
port defaults to the AC voltage type. The utility port adds no extra electrical attributes
beyond the abstract base and the two blocks.

## Electrical

The `electrical` section holds the single port.

- `ports` (array of 1 port): see above.

## Example

See [`examples/testUtility.json`](../examples/testUtility.json).

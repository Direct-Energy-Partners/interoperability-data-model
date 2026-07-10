# Grounding

A grounding component represents an earth connection or grounding arrangement, providing a
defined reference point and a path for fault and leakage currents to earth. In a DC system it
sets the earthing configuration of a circuit and absorbs current flowing into earth through its
single input port.

- Type key: `grounding`
- Indicator: `GND`
- Plural: Groundings
- Ports: 1, input only, carrying both an AC and a DC block.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A grounding component has exactly one port. Its `powerFlowDirection` is fixed to `input`, since
current flows into the earth connection. On top of the abstract port base (features, terminal,
wire size) the port carries the standard AC block and the standard DC block, each extended with
a grounding configuration, plus one extra port level attribute.

- AC block: the standard AC fields (voltage, current, power, frequency, power factor,
  configuration, earthing) plus `groundingConfiguration` (enum, default `TN-S`), one of `TN-S`,
  `TN-C`, `IT`, `TT`, `unearthed`.
- DC block: the standard DC fields (voltage, current, power, configuration, earthing) plus
  `groundingConfiguration` (enum, default `TN-S`), one of `TN-S`, `IT`, `unearthed`.
- `earthingImpedance` (value, unit `ohm`): the impedance of the connection to earth.

## Electrical

The `electrical` section holds only the port.

- `ports` (tuple of 1 port): see above.

## Example

See [`examples/testGrounding.json`](../examples/testGrounding.json).

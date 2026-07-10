# Disconnect

A disconnect is a manually or remotely operated switch that isolates a section of a circuit for
maintenance or safety. In a DC system it provides a visible break in the conductor, breaking
the circuit on both sides when opened so downstream equipment can be safely de-energised.

- Type key: `disconnect`
- Indicator: `Q`
- Plural: Disconnects
- Ports: 2, shown as a single port in the diagram. Each port carries both an AC and a DC block.
  Power flow may be input, output or bidirectional.
- Acts as: switchgear

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A disconnect has exactly two ports, which are displayed as a single port in the diagram. The
two ports share the same definition and are kept in sync. Each port defaults to
`powerFlowDirection` `bidirectional`. On top of the abstract port base (features, terminal,
wire size) each port carries the standard AC block and the standard DC block, each extended
with control methods:

- AC block: the standard AC fields (voltage, current, power, frequency, power factor,
  configuration, earthing) plus `controlMethods` (array).
- DC block: the standard DC fields (voltage, current, power, configuration, earthing) plus
  `controlMethods` (array).

The `controlMethods` array accepts the AC and DC control methods listed in
[common attributes](./common.md): `constant-voltage-frequency`,
`constant-active-reactive-power`, `uncontrolled`, `constant-voltage`, `constant-current`,
`constant-power`, `droop-voltage`, `power-voltage`, `maximum-power-point-tracking`.

## Electrical

The `electrical` section holds the ports and a feature flag object.

- `ports` (tuple of 2 ports): see above.
- `features` (object):
  - `feedbackSignal` (boolean, default `false`): whether the disconnect reports its open or
    closed state.
  - `fuse` (boolean, default `false`): whether the disconnect includes an integrated fuse.

## Example

See [`examples/testDisconnect.json`](../examples/testDisconnect.json).

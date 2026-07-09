# Load

A load is a generic power consuming component. It represents any device that draws power from
the system without a more specific component type fitting it. In a DC system it sits at the
consuming end of the bus and is balanced against generation and storage. The IDM models a load
as a single input port that can carry AC, DC, or both.

- Type key: `load`
- Indicator: `LOAD`
- Plural: Loads
- Ports: 1, input only, carries an AC block and a DC block.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

A load has exactly one port. The port has its power flow direction fixed to `input`, since the
load consumes power. The port carries both an AC block and a DC block. On top of the abstract
port base (features, terminal, wire size) and the standard AC and DC blocks (voltage, current,
power, configuration, earthing, and for AC also frequency and power factor), the load port
adds:

- `controlMethods` on the AC block: subset of `constant-voltage-frequency`,
  `constant-active-reactive-power`, `uncontrolled`.
- `controlMethods` on the DC block: subset of `constant-voltage`, `constant-current`,
  `constant-power`, `droop-voltage`, `power-voltage`, `maximum-power-point-tracking`,
  `uncontrolled`.
- `capacitance` (value, unit `F`): port capacitance.
- `equivalentSeriesResistance` (value, unit `ohm`): equivalent series resistance.

The allowed control methods at the definition level are `constant-power` and `power-voltage`.

## Electrical

The `electrical` section holds the single port.

- `ports` (array of 1 port): see above.

## Example

See [`examples/testLoad.json`](examples/testLoad.json).

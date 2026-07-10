# Capacitor

A capacitor stores energy in an electric field and is used in DC systems to smooth voltage,
filter ripple and supply transient current. The IDM models a capacitor as a single
bidirectional DC port with capacitance and series resistance attributes.

- Type key: `capacitor`
- Indicator: `C`
- Plural: Capacitors
- Ports: 1, bidirectional, DC

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A capacitor has exactly one port. The port is DC only and fixed to a bidirectional power flow
direction, since a capacitor both absorbs and releases current. On top of the abstract port
base (features, terminal, wire size) and the standard DC block (voltage, current, power,
configuration, earthing), the capacitor port adds:

- `capacitance` (value, unit `F`): the capacitance of the device.
- `equivalentSeriesResistance` (value, unit `ohm`): internal series resistance.
- `reverseDiode` (boolean, default `false`): whether a reverse diode is present.

## Electrical

The `electrical` section holds the single port.

- `ports` (tuple of 1 port): see above.

## Example

See [`examples/testCapacitor.json`](../examples/testCapacitor.json).

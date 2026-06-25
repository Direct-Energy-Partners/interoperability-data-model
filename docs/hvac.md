# HVAC

An HVAC unit covers heating, ventilation and air conditioning equipment. In a DC system it is
a controllable load that draws power to condition the air, and it is often sized and scheduled
against on site generation and storage. The IDM models an HVAC unit as one or more input ports
that can carry AC, DC, or both.

- Type key: `hvac`
- Indicator: `HVAC`
- Plural: HVACs
- Ports: 1 or more, input only, each port carries an AC block and a DC block.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

An HVAC unit has one or more ports (minimum 1, no fixed maximum). Every port has its power flow
direction fixed to `input`, since the unit consumes power. Each port carries both an AC block
and a DC block. On top of the abstract port base (features, terminal, wire size) and the
standard AC and DC blocks (voltage, current, power, configuration, earthing, and for AC also
frequency and power factor), the HVAC port adds:

- `controlMethods` on the AC block: subset of `constant-voltage-frequency`,
  `constant-active-reactive-power`, `uncontrolled`.
- `controlMethods` on the DC block: subset of `constant-voltage`, `constant-current`,
  `constant-power`, `droop-voltage`, `power-voltage`, `maximum-power-point-tracking`,
  `uncontrolled`.
- `capacitance` (value, unit `F`): port capacitance.
- `equivalentSeriesResistance` (value, unit `ohm`): equivalent series resistance.
- `purpose` (enum, nullable): subset of `battery`, `solar`. Indicates the intended source the
  port is paired with. Defaults to `null`.

The allowed control methods at the definition level are `constant-power` and `power-voltage`.

## Electrical

The `electrical` section holds the port array.

- `ports` (array of 1 or more ports): see above.

## Example

See [`examples/testHvac.json`](../examples/testHvac.json).

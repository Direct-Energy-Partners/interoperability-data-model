# Fuel Cell

A fuel cell converts the chemical energy of a fuel, such as hydrogen, directly into electrical
energy through an electrochemical reaction. In a DC system it is a generation source, delivering
power outward to the rest of the system through a single output port.

- Type key: `fuelCell`
- Indicator: `FC`
- Plural: Fuel Cells
- Ports: 1, output only, carrying both an AC and a DC block.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

A fuel cell has exactly one port. Its `powerFlowDirection` is fixed to `output`, since the fuel
cell only delivers power. On top of the abstract port base (features, terminal, wire size) the
port carries the standard AC block and the standard DC block, each extended with control
methods, plus a few storage style attributes:

- AC block: the standard AC fields (voltage, current, power, frequency, power factor,
  configuration, earthing) plus `controlMethods` (array).
- DC block: the standard DC fields (voltage, current, power, configuration, earthing) plus
  `controlMethods` (array).
- `capacitance` (value, unit `F`): port capacitance.
- `equivalentSeriesResistance` (value, unit `ohm`): internal series resistance.
- `isolated` (boolean, nullable, default `null`): whether the port is galvanically isolated.
- `parallelableCapacity` (number, minimum 1, default 1): how many units may be paralleled.

The control methods allowed for this type are `constant-power`, `power-voltage`,
`constant-voltage`, `constant-voltage-frequency` and `constant-active-reactive-power`. The full
set of control method enum values is listed in [common attributes](./common.md).

## Electrical

The `electrical` section holds only the port.

- `ports` (tuple of 1 port): see above.

## Example

See [`examples/testFuelCell.json`](../examples/testFuelCell.json).

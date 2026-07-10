# Generator

A generator converts mechanical energy into electrical energy, for example a diesel or gas
gen-set driving an alternator. In a DC system it is a generation source, delivering power
outward to the rest of the system through a single output port.

- Type key: `generator`
- Indicator: `G`
- Plural: Generators
- Ports: 1, output only, carrying both an AC and a DC block.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A generator has exactly one port. Its `powerFlowDirection` is fixed to `output`, since the
generator only delivers power. On top of the abstract port base (features, terminal, wire size)
the port carries the standard AC block and the standard DC block, each extended with control
methods, plus a few additional attributes:

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

See [`examples/testGenerator.json`](../examples/testGenerator.json).

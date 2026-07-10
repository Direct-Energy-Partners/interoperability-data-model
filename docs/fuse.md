# Fuse

A fuse protects a circuit by melting a conductive element and breaking the circuit when the
current exceeds a rated value for long enough. In a DC system it provides overcurrent and short
circuit protection, passing current through from one terminal to the other until it clears.

- Type key: `fuse`
- Indicator: `F`
- Plural: Fuses
- Ports: 2, shown as a single port in the diagram. Each port carries both an AC and a DC block.
  Power flow may be input, output or bidirectional.

A fuse does not carry the shared communication section, as it is a passive protective device.
See [common attributes](./common.md) for the rest of the shared base every component carries
(identification, compliance, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A fuse has exactly two ports, which are displayed as a single port in the diagram. The two
ports share the same definition and are kept in sync. Each port defaults to
`powerFlowDirection` `bidirectional`. On top of the abstract port base (features, terminal,
wire size) each port carries an AC block and a DC block extended with short circuit ratings, and
two extra port level attributes.

The AC block has the standard AC fields (voltage, current, frequency, power factor,
configuration), with the standard AC `power` and `earthingConfigurations` fields omitted, plus:

- `instantaneousShortCircuitCurrentUL` (value, unit `A`): UL instantaneous short circuit
  current rating.
- `serviceShortCircuitBreakingCapacityIEC` (value, unit `A`): IEC service short circuit
  breaking capacity.
- `ultimateShortCircuitBreakingCapacityIEC` (value, unit `A`): IEC ultimate short circuit
  breaking capacity.
- `criticalClearingTime` (value, unit `s`): time to clear the fault.
- `minimumBreakingCapacity` (value, unit `A`): minimum current the fuse can interrupt.

The DC block has the standard DC fields (voltage, current, configuration), with the standard DC
`power` and `earthingConfigurations` fields omitted, plus the same short circuit ratings as the
AC block and additionally:

- `maximumTimeConstant` (value, unit `s`): the maximum circuit time constant the fuse is rated
  for.

Each port also adds:

- `numberOfPoles` (number, positive, default 2): the number of poles.
- `overvoltageCategory` (number, optional): the overvoltage category the port is rated for.

## Electrical

The `electrical` section holds the ports and the let-through energy characteristics.

- `ports` (tuple of 2 ports): see above.
- `standards` (string array): fuse specific standards.
- `isolationVoltage` (value, unit `V`): isolation voltage.
- `meltingI2t` (value, unit `A²•s`): melting I squared t.
- `arcingI2t` (value, unit `A²•s`): arcing I squared t.
- `totalClearingI2t` (value, unit `A²•s`): total clearing I squared t.
- `i2tCurve` (array): the let-through energy curve, each entry an object with `tPreArc`
  (number) and `sumI2t` (number).

## Example

See [`examples/testFuse.json`](../examples/testFuse.json).

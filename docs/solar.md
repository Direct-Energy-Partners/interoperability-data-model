# Solar Panel

A solar panel converts incident sunlight into DC electrical power through the photovoltaic
effect. In a DC system it is a generation source that feeds the bus, typically through a
converter that tracks its maximum power point. The IDM models a solar panel as a single DC
output port plus the photovoltaic operating characteristics.

- Type key: `solar`
- Indicator: `PV`
- Plural: Solar Panels
- Ports: 1, output, DC

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

A solar panel has exactly one port. The port is DC only and fixed to output power flow, since
the panel only sources power. On top of the abstract port base (features, terminal, wire size)
and the standard DC block (voltage, current, power, configuration, earthing), the solar port
adds these photovoltaic characteristics to the DC block:

- `maximumPowerPointCurrent` (value, unit `A`): current at the maximum power point.
- `maximumPowerPointVoltage` (value, unit `V`): voltage at the maximum power point.
- `openCircuitVoltage` (value, unit `V`): voltage with no load connected.
- `shortCircuitCurrent` (value, unit `A`): current with the output shorted.

The allowed port control methods are `constant-power`, `constant-current` and `power-voltage`.

## Electrical

The `electrical` section holds the port and the cell technology.

- `ports` (tuple of exactly 1 port): see above.
- `solarTechnologies` (array): the cell technology, subset of `monocrystalline`,
  `polycrystalline`, `perc`, `thin-film`, `perovskite`, `bifacial`, `hit`, `cigs`, `cdte`,
  `amorphous`, `building-integrated photovoltaics`. Defaults to empty.

## Example

See [`examples/testSolar.json`](examples/testSolar.json).

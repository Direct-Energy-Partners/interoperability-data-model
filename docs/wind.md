# Wind

A wind turbine converts wind energy into electrical power, feeding it into the system. It is a
generation source, so its single port only delivers power outward. In the IDM a wind component
is modelled as one output port that carries both an AC and a DC block.

- Type key: `wind`
- Indicator: `WIND`
- Plural: Wind
- Ports: 1, output, carries both an AC and a DC block

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

A wind component has exactly one port, fixed to output power flow direction, since the turbine
only delivers power to the system. The port carries both an AC block (voltage, current, power,
frequency, power factor, configuration, earthing) and a DC block (voltage, current, power,
configuration, earthing) on top of the abstract port base (features, terminal, wire size). The
wind port adds no extra electrical attributes beyond the abstract base and the two blocks.

## Electrical

The `electrical` section holds the single port.

- `ports` (array of 1 port): see above.

## Example

See [`examples/testWind.json`](examples/testWind.json).

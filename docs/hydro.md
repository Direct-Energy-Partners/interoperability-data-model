# Hydro

A hydro unit generates electrical power from moving water, for example a micro hydro turbine on
a stream or penstock. In a DC system it acts as a source that feeds power into the bus. The IDM
models a hydro unit as a single output port that can carry AC, DC, or both.

- Type key: `hydro`
- Indicator: `HYDRO`
- Plural: Hydro
- Ports: 1, output only, carries an AC block and a DC block.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

A hydro unit has exactly one port. The port has its power flow direction fixed to `output`,
since the unit supplies power. The port carries both an AC block and a DC block. Beyond the
abstract port base (features, terminal, wire size) and the standard AC and DC blocks (voltage,
current, power, configuration, earthing, and for AC also frequency and power factor), the hydro
port adds no extra port level attributes.

## Electrical

The `electrical` section holds the single port.

- `ports` (array of 1 port): see above.

## Example

See [`examples/testHydro.json`](examples/testHydro.json).

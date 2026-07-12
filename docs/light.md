# Light

A light is a lighting fixture or luminaire that consumes power to produce illumination. In a DC
system it is a small input load, often run directly from a low voltage DC bus. The IDM models a
light as a single input port that can carry AC, DC, or both.

- Type key: `light`
- Indicator: `LIGHT`
- Plural: Lights
- Ports: 1, input only, carries an AC block and a DC block.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance) and for the shared port model.

## Ports

A light has exactly one port. The port has its power flow direction fixed to `input`, since the
light consumes power. The port carries both an AC block and a DC block. Beyond the abstract
port base (features, terminal, wire size) and the standard AC and DC blocks (voltage, current,
power, configuration, earthing, and for AC also frequency and power factor), the light port
adds no extra port level attributes.

## Electrical

The `electrical` section holds the single port.

- `ports` (array of 1 port): see above.

## Example

See [`examples/testLight.json`](../examples/testLight.json).

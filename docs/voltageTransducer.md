# Voltage Transducer

A voltage transducer measures voltage and converts it into a scaled signal for metering,
protection or control. It is a sensing device rather than a power path, so it presents a single
input port. In the IDM a voltage transducer is modelled with one input port plus accuracy,
response time and isolation voltage ratings.

- Type key: `voltageTransducer`
- Indicator: `PT`
- Plural: Voltage Transducers
- Ports: 1, input, carries both an AC and a DC block

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance) and for the shared port model.

## Ports

A voltage transducer has exactly one port, labelled `Input Port`, with input power flow
direction. The port carries both an AC block (voltage, current, power, frequency, power factor,
configuration, earthing) and a DC block (voltage, current, power, configuration, earthing) on
top of the abstract port base (features, terminal, wire size). On top of those, the input port
adds:

- `overvoltageCategory` (number, nullable, default `null`): the overvoltage (installation)
  category of the input.

## Electrical

The `electrical` section holds the input port and the measurement ratings.

- `ports` (array of 1 port): see above.
- `isolationVoltage` (value, unit `V`): rated dielectric withstand voltage of the input.
- `accuracy` (value, unit `%`): measurement accuracy.
- `responseTime` (value, unit `s`): time to respond to a change at the input.

## Example

See [`examples/testVoltageTransducer.json`](../examples/testVoltageTransducer.json).

# Current Transducer

A current transducer measures the current flowing through a conductor and converts it into a
proportional output signal for metering, monitoring and protection. In a DC system it provides
the current feedback that controllers and meters rely on, while passing the measured circuit
through from input to output.

- Type key: `currentTransducer`
- Indicator: `CT`
- Plural: Current Transducers
- Ports: 2 (an input port and an output port), each carrying both an AC and a DC block. Power
  flow may be input, output or bidirectional.

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

A current transducer has exactly two ports, labelled `Input Port` and `Output Port`. The first
port defaults to `powerFlowDirection` `input` and the second to `output`. Each port carries
both a standard AC block (voltage, current, power, frequency, power factor, configuration,
earthing) and a standard DC block (voltage, current, power, configuration, earthing). On top of
the abstract port base (features, terminal, wire size) each port adds:

- `overvoltageCategory` (number, optional): the overvoltage category the port is rated for.

## Electrical

The `electrical` section holds the metrology attributes.

- `ports` (tuple of 2 ports): see above.
- `isolationVoltage` (value, unit `V`): the isolation voltage between the primary circuit and
  the output.
- `accuracy` (value, unit `%`): measurement accuracy.
- `responseTime` (value, unit `s`): time to respond to a change in the measured current.

## Example

See [`examples/testCurrentTransducer.json`](examples/testCurrentTransducer.json).

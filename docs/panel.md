# Panel Switchboard

A panel switchboard is an assembly in which devices are mounted, such as circuit breakers,
contactors and meters, for the purpose of protection and control. It is used to distribute
electric power to circuits. In a DC system it behaves as a bus, tying multiple connections
together. It can have any number of AC and DC ports.

- Type key: `panel`
- Indicator: `A`
- Plural: Panels Switchboards
- Ports: 1 or more, each input, output or bidirectional, each port carries an AC block and a DC
  block.
- Acts as: bus

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance, files,
images and metadata) and for the shared port model.

## Ports

A panel switchboard has one or more ports (minimum 1, no fixed maximum). Each port may be
`input`, `output` or `bidirectional`, and the default direction is `bidirectional`. Each port
carries both an AC block and a DC block. Beyond the abstract port base (features, terminal, wire
size) and the standard AC and DC blocks (voltage, current, power, configuration, earthing, and
for AC also frequency and power factor), the panel port adds no extra port level attributes.

## Electrical

The `electrical` section holds the port array.

- `ports` (array of 1 or more ports): see above.

## Example

See [`examples/testPanel.json`](examples/testPanel.json).

# Transfer switch

A transfer switch selects which of two sources feeds a load, switching the connection from one
to the other. In a DC system it is used to move a load between, for example, a primary supply
and a backup. The IDM models a transfer switch as three ports (displayed as a single port),
kept electrically in sync, plus an isolation rating.

- Type key: `transferSwitch`
- Indicator: `Q`
- Plural: Transfer switches
- Ports: 3, input, output or bidirectional, AC and DC

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A transfer switch has exactly three ports, each defaulting to bidirectional power flow but
each settable to input or output. The AC and DC blocks of the first port are kept in sync with
those of the other two ports, and the three ports are displayed as a single port in the user
interface. Each port carries both an AC block and a DC block (as described in the shared port
model). On top of the abstract port base (features, terminal, wire size) and the AC and DC
blocks, each transfer switch port adds to its AC block:

- `controlMethods` (array): the AC control methods the port supports, subset of
  `constant-voltage-frequency`, `constant-active-reactive-power`, `uncontrolled`.

## Electrical

The `electrical` section holds the three ports, device standards and the isolation rating.

- `ports` (tuple of exactly 3 ports): see above.
- `standards` (string array): standards the switch complies with.
- `isolationVoltage` (value, unit `V`): voltage the switch isolates against between sources.

## Example

See [`examples/testTransferSwitch.json`](../examples/testTransferSwitch.json).

# Precharge

A precharge limits inrush current when a capacitive load or DC bus is first energised. It
inserts a resistance into the circuit during the initial charge so that voltage rises in a
controlled way, then is bypassed for normal operation. The IDM models a precharge as two
bidirectional ports (displayed as a single port) plus a series resistance.

- Type key: `precharge`
- Indicator: `PRE`
- Plural: Precharges
- Ports: 2, both bidirectional, AC and DC

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A precharge has exactly two ports, both fixed to bidirectional power flow. The two ports are
kept in sync (port 1 mirrors port 0) and the pair is displayed as a single port in the user
interface. Each port carries both an AC block and a DC block (as described in the shared port
model). The precharge port adds no extra port level attributes beyond the abstract port base
(features, terminal, wire size) and the AC and DC blocks.

## Electrical

The `electrical` section holds the port pair and the precharge resistance.

- `ports` (tuple of exactly 2 ports): see above.
- `resistance` (value, unit `ohm`): series resistance used to limit inrush current.

## Example

See [`examples/testPrecharge.json`](../examples/testPrecharge.json).

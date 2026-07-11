# EV Charger

An EV charger (also referred to as an EV) delivers power to an electric vehicle and, where
supported, draws power back from it. In a DC system it acts as a converter between the system
buses and the vehicle, managing voltage, current and the physical charging connectors. The IDM
models an EV charger as a flexible set of converting ports plus a list of charging ports that
describe the vehicle facing connectors.

- Type key: `charger`
- Indicator: `CHG`
- Plural: EV Chargers
- Ports: 1 or more, each input, output or bidirectional, AC and DC
- Acts as: converter

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance) and for the shared port model.

## Ports

A charger has a dynamic number of ports: at least one, with no upper bound. Each port defaults
to a bidirectional power flow direction, supporting vehicle to grid style operation as well as
charging. Every port carries both an AC block and a DC block (the DC block defaults to a
`unipolar` configuration). Each block adds `controlMethods` on top of the standard fields. The
allowed control methods for a charger are `constant-power`, `power-voltage` and
`constant-voltage`.

On top of the abstract port base (features, terminal, wire size) and the AC and DC blocks, each
charger port adds:

- `controlMethods` (array, per AC and DC block, default `[]`): the control strategies the port
  can use. AC values are `constant-voltage-frequency`, `constant-active-reactive-power`,
  `uncontrolled`. DC values are `constant-voltage`, `constant-current`, `constant-power`,
  `droop-voltage`, `power-voltage`, `maximum-power-point-tracking`, `uncontrolled`.
- `capacitance` (value, unit `F`): port capacitance.
- `equivalentSeriesResistance` (value, unit `ohm`): port series resistance.
- `isolated` (boolean, nullable, default `null`): whether the port is galvanically isolated.
- `parallelableCapacity` (number, minimum 1, default 1): how many units may be paralleled on
  this port.
- `purpose` (enum, nullable, default `null`): the intended role of the port, one of `battery`,
  `converter`, `solar`, `panel`, `charger`, `generator`.

## Electrical

The `electrical` section holds the system facing ports plus the vehicle facing charging ports.

- `ports` (array, default 1 port): see above.
- `standards` (string array): charger specific standards.
- `chargingPorts` (array, default one AC port): the physical vehicle connectors. Each entry has:
  - `id` (string): generated identifier.
  - `connector` (enum, nullable, default `null`): connector type, one of `ccs1`, `ccs2`,
    `chademo`, `tesla`, `type1`, `type2`, `nacs`.
  - `voltageType` (enum, nullable, default `null`): `AC` or `DC`.
  - `voltage` (min, max, unit `V`): voltage range.
  - `current` (min, max, unit `A`): current range.
  - `power` (min, nom, max, unit `W`): power range.
  - `features` (array, default `[]`): bidirectional charging features, subset of `v2g`
    (vehicle to grid), `v2h` (vehicle to home), `v2l` (vehicle to load), `v2x` (vehicle to
    anything).
- `isolationVoltage` (value, unit `V`): rated isolation voltage.

## Environmental

The EV charger uses the environmental section with `coolingMethod` added (one of `passive`,
`forced-air`, `liquid`, `none`, default `none`). All other environmental fields are as
described in [common attributes](./common.md).

## Example

See [`examples/testCharger.json`](../examples/testCharger.json).

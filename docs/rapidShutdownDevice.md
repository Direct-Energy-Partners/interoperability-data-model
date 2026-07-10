# Rapid Shutdown Device

A rapid shutdown device is a device that is used to rapidly shut down the flow of electricity
from a photovoltaic system to ensure the safety of first responders. In a DC system it sits
between the array and the rest of the installation and de-energises the conductors on command.
The IDM models a rapid shutdown device as two ports (displayed as a single port) that pass
power through.

- Type key: `rapidShutdownDevice`
- Indicator: `RSD`
- Plural: Rapid Shutdown Devices
- Ports: 2, input, output or bidirectional, AC and DC
- Can serve as: contactor, disconnect

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance) and for the shared port model.

## Ports

A rapid shutdown device has exactly two ports. The first port defaults to input and the second
to output, though each may also be set to bidirectional. The two ports are kept in sync (port 1
mirrors port 0) and the pair is displayed as a single port in the user interface. Each port
carries both an AC block and a DC block (as described in the shared port model). The rapid
shutdown device port adds no extra port level attributes beyond the abstract port base
(features, terminal, wire size) and the AC and DC blocks.

## Electrical

The `electrical` section holds the port pair and device standards. In addition, the type
carries a top level `canServeAs` key.

- `ports` (tuple of exactly 2 ports): see above.
- `standards` (string array): standards the device complies with.
- `canServeAs` (array): component types this device can stand in for, drawn from `contactor`
  and `disconnect`. Defaults to empty.

## Environmental

The rapid shutdown device uses the environmental section with `coolingMethod` added (one of
`passive`, `forced-air`, `liquid`, `none`, default `none`). All other environmental fields are
as described in [common attributes](./common.md).

## Example

See [`examples/testRapidShutdownDevice.json`](../examples/testRapidShutdownDevice.json).

# Interoperability Data Model documentation

The Interoperability Data Model (IDM) describes electrical components in a common, machine
readable form so that tools across the DC ecosystem can exchange product data. The model is
expressed as JSON Schema (draft-07), one file per component type under `schema/`, with example
instances under `examples/`.

The schemas are the source of truth. Each page below documents one component type and its
attributes.

## Start here

- [Common attributes](./common.md): the shared base that every component carries
  (identification, compliance, communication, environmental, mechanical, performance, files,
  images and metadata) and the shared port model (AC and DC blocks, terminal, wire size,
  features, earthing and control methods).

## Component types

- [Battery](./battery.md) (`battery`, BAT)
- [Cable](./cable.md) (`cable`, WIRE)
- [Capacitor](./capacitor.md) (`capacitor`, C)
- [Circuit Breaker](./breaker.md) (`breaker`, Q)
- [Combiner Box](./combinerBox.md) (`combinerBox`, A)
- [Contactor](./contactor.md) (`contactor`, K)
- [Converter](./converter.md) (`converter`, U)
- [Current Transducer](./currentTransducer.md) (`currentTransducer`, CT)
- [Diode](./diode.md) (`diode`, D)
- [Disconnect](./disconnect.md) (`disconnect`, Q)
- [EV Charger](./charger.md) (`charger`, CHG)
- [Fuel Cell](./fuelCell.md) (`fuelCell`, FC)
- [Fuse](./fuse.md) (`fuse`, F)
- [Generator](./generator.md) (`generator`, G)
- [Grounding](./grounding.md) (`grounding`, GND)
- [HVAC](./hvac.md) (`hvac`, HVAC)
- [Hydro](./hydro.md) (`hydro`, HYDRO)
- [Light](./light.md) (`light`, LIGHT)
- [Load](./load.md) (`load`, LOAD)
- [Meter](./meter.md) (`meter`, P)
- [Motor](./motor.md) (`motor`, M)
- [Panel Switchboard](./panel.md) (`panel`, A)
- [Power Distribution Unit](./powerDistributionUnit.md) (`powerDistributionUnit`, PDU)
- [Precharge](./precharge.md) (`precharge`, PRE)
- [Rapid Shutdown Device](./rapidShutdownDevice.md) (`rapidShutdownDevice`, RSD)
- [Solar Panel](./solar.md) (`solar`, PV)
- [Transfer Switch](./transferSwitch.md) (`transferSwitch`, Q)
- [Transformer](./transformer.md) (`transformer`, T)
- [Utility](./utility.md) (`utility`, GRID)
- [Voltage Transducer](./voltageTransducer.md) (`voltageTransducer`, PT)
- [Wind](./wind.md) (`wind`, WIND)

## How to read a component page

Each page opens with a short description and a summary block (type key, indicator, plural, port
configuration). It then documents the ports and the component specific electrical attributes.
Anything not listed on the page comes from the [common attributes](./common.md) shared by all
types.

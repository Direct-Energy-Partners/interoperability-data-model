# Cable

A cable carries current between two points in a system. It is described by its conductors,
insulation, screening and the per unit length electrical properties that determine voltage drop
and impedance. Unlike most components, a cable is not placed inline as a node in a diagram, so
it is not assigned diagram ports. Instead it captures conductor and construction attributes
that the wiring of a design draws on.

- Type key: `cable`
- Indicator: `WIRE`
- Plural: Cables
- Ports: none (diagram use is disabled)

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance and files) and for the shared port model.

## Ports

A cable has no diagram ports. Diagram use is disabled, because a cable is the wiring between
components rather than a component placed inline in a diagram. The `electrical.ports` array
still carries a single abstract port record (defaulting to bidirectional power flow, with an AC
and a DC block) so the cable can describe the connection it forms, but no ports are exposed for
placement in a diagram.

## Electrical

The cable specific attributes are split across `electrical`, `mechanical` and `environmental`.

`electrical` (object).

- `ports` (array): a single abstract port record, see above.
- `wireSize` (wire size code, nullable, default `null`): conductor cross sectional area code
  from the cross sectional area series (for example `1.5`, `2.5`, `4`, up to `1016`).
- `cores` (enum, default `single`): one of `single`, `multi`, `multi-pe`.
- `operatingVoltage` (object):
  - `toEarth` (value, unit `V`): operating voltage to earth.
  - `betweenLines` (value, unit `V`): operating voltage between lines.
- `numberOfConductors` (integer, 1 to 4, nullable, default `null`): number of conductors.
- `hasPE` (boolean, default `false`): whether a protective earth conductor is present.
- `voltageTypes` (array): subset of `AC`, `DC`.
- `resistancePerLength` (value, unit `ohm/m`, default unit `ohm/m`): conductor resistance per
  unit length. Other accepted units: `ohm/km`, `ohm/ft`, `mohm/m`, `mohm/km`, `mohm/ft`.
- `inductancePerLength` (value, unit `H/m`, default unit `H/m`): conductor inductance per unit
  length. Other accepted units: `uH/m`, `uH/km`, `uH/ft`, `mH/m`, `mH/km`, `mH/ft`, `H/km`,
  `H/ft`.
- `cpr` (object): Construction Products Regulation reaction to fire classification.
  - `class` (enum, nullable, default `null`): one of `Aca`, `B1ca`, `B2ca`, `Cca`, `Dca`,
    `Eca`, `Fca`.
  - `smokeProduction` (enum, nullable, default `null`): one of `s1`, `s1a`, `s1b`, `s2`, `s3`.
  - `flamingDroplets` (enum, nullable, default `null`): one of `d0`, `d1`, `d2`.
  - `acidity` (enum, nullable, default `null`): one of `a1`, `a2`, `a3`.
- `intertrippingWireSize` (number, nullable, default `null`): intertripping conductor cross
  section in mm2.

`mechanical` (object). For a cable the mechanical section is replaced by conductor and
insulation construction.

- `conductorMaterial` (enum, default `copper`): one of `aluminum`, `copper`.
- `conductorFlexibility` (enum, nullable, default `null`): one of `solid`, `stranded`,
  `class1`, `class2`, `class3`, `class4`, `class5`, `class6`.
- `insulationMaterial` (enum, default `PVC`): one of `PVC`, `XLPE`.
- `screen` (enum, nullable, default `null`): one of `none`, `yes`, `aluminiumPet`,
  `aluminiumPetDrain`, `copperBraid`, `tinnedCopperBraid`, `copperTape`, `steelWireArmour`,
  `copperWireScreen`, `tinnedCopperWireScreen`, `foilBraid`, `overall`, `individual`,
  `individualAndOverall`.

`environmental` (object). For a cable the environmental section is replaced by installation
attributes.

- `installationTemperature` (min, max, unit `K`): temperature at the installation.
- `use` (array, default empty): subset of `indoor`, `outdoor`.

The cable type omits the common `performance` and `communication` sections (both are present
but empty), and replaces the common `mechanical` and `environmental` sections with the cable
specific objects above.

## Example

See [`examples/testCable.json`](../examples/testCable.json).

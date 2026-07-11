# Combiner Box

A combiner box combines the output of multiple strings of photovoltaic panels into a single DC
output. In a DC system it gathers several incoming source feeds and merges them onto one
outgoing connection, simplifying the wiring between an array and downstream equipment. The IDM
models a combiner box as a flexible set of ports, typically one output and several inputs.

- Type key: `combinerBox`
- Indicator: `A`
- Plural: Combiner Boxes
- Ports: 2 or more, each input or output, AC and DC

See [common attributes](./common.md) for the shared base every component carries
(identification, compliance, communication, environmental, mechanical, performance) and for the shared port model.

## Ports

A combiner box has a dynamic number of ports: at least two, with no upper bound. Ports are
input or output (not bidirectional); the default layout is one output port followed by two
input ports. Every port carries both an AC block and a DC block (each defaulting to enabled).

On top of the abstract port base (features, terminal, wire size) and the standard AC and DC
blocks, each combiner box port adds:

- `description` (string, default empty): free text label for the port.
- `purpose` (enum, nullable, default `null`): the intended role of the port, one of `battery`,
  `converter`, `solar`, `panel`, `charger`, `generator`.

## Electrical

The `electrical` section holds the ports.

- `ports` (array, minimum 2): see above.

The component also carries a top level `compatibleProducts` key:

- `compatibleProducts` (array of component ids, default `[]`): products known to be compatible
  with this combiner box.

## Example

See [`examples/testCombinerBox.json`](../examples/testCombinerBox.json).

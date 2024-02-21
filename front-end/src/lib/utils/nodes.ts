const nodesOrderMap : Map<string,number> = new Map(
  [
    ['Left Wing Cable', 0],
    ['Other Cable', 1],
    ['Hard Broadcast News', 2],
    ['Soft Broadcast News', 3],
    ['Spanish News', 4],
    ['Right Wing Cable', 5],
  ]
)

const nodesLabels : Map<string,number> = new Map(
  [
    ['Left Wing Cable', 'Partisan Left Cable'],
    ['Right Wing Cable', 'Partisan Right Cable'],
  ]
)

export default nodesOrderMap
export { nodesLabels }

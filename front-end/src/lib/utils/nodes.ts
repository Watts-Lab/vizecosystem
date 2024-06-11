const nodesOrderMap : Map<string,number> = new Map(
  [
    ['Partisan Cable (left)', 0],
    ['Other Cable', 1],
    ['Hard Broadcast News', 2],
    ['Soft Broadcast News', 3],
    ['Spanish News', 4],
    ['Partisan Cable (right)', 5],
  ]
)

const nodesLabels : Map<string,number> = new Map(
  [
    ['Partisan Cable (left)', 'Partisan Cable (left)'],
    ['Partisan Cable (right)', 'Partisan Cable (right)'],
  ]
)

export default nodesOrderMap
export { nodesLabels }

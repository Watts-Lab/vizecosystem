export default function(data : any[], cols : string[]) {

  // console.log(data)

  return data.map((d, i) => {
    const total = cols.reduce((prev : number, curr : string) => {
      return prev + d[curr]
    }, 0)
    const pcts = cols.reduce((prev : object, curr : string) => {
      prev[curr] = d[curr] / total
      return prev
    }, {})
    
    return { ...d, ...pcts }
  })
}
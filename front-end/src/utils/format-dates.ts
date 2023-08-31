import { timeFormat } from 'd3-time-format'

const formatMonth = timeFormat('%b-%y')
const formatYear = timeFormat('%Y')

export { formatMonth, formatYear }
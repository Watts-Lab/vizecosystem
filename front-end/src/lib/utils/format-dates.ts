import { timeFormat } from 'd3-time-format'

const formatMonth = timeFormat('%b %Y')
const formatYear = timeFormat('%Y')

export { formatMonth, formatYear }
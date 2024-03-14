import { format } from 'd3-format'

const formatPct = (n) => {
    return format(`.${n}~%`)
}

const formatThousands = format(',.0s')
const formatThousands2SI = format(',.2s')
const formatThousandsComma = format(',.0f')

const formatPositiveNegative = format('+,.2s')

function formatOrdinal(n) {
    var s = ["th", "st", "nd", "rd"],
        v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  }

export { formatPct, formatThousands, formatThousands2SI, formatThousandsComma, formatPositiveNegative, formatOrdinal }
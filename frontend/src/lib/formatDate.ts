import { months, monthsPlural } from './months'

export function formatDate(
    date: Date,
    format = 'DD.MM.YYYY',
    options: { padDay?: boolean; monthPlural?: boolean } = {
        padDay: true,
        monthPlural: false,
    }
) {
    date = new Date(date)
    format = format.toLowerCase()

    const day = date.getDate()
    const month = date.getMonth()
    const year = date.getFullYear()

    const dayStr = options.padDay ? (day + '').padStart(2, '0') : day + ''
    const monthStr = (options.monthPlural ? monthsPlural : months)[month]
    const monthShort =
        monthStr.length > 4 ? monthStr.substring(0, 3) + '.' : monthStr

    format = format.replaceAll(/y+/gm, year + '')
    format = format.replaceAll(/d+/gm, dayStr)
    format = format.replaceAll(/m+_str/gm, monthStr)
    format = format.replaceAll(/m+_short/gm, monthShort)
    format = format.replaceAll(/m+/gm, (month + 1 + '').padStart(2, '0'))

    return format
}

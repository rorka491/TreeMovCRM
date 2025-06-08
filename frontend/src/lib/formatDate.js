const monthes = [
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
]

const monthsPlural = [
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'октября',
    'ноября',
    'декабря',
]

export function formatDate(
    date,
    format = 'DD.MM.YYYY',
    options = { padDay: false, monthPlural: false }
) {
    date = new Date(date)
    format = format.toLowerCase()

    const day = date.getDate()
    const month = date.getMonth()
    const year = date.getFullYear()

    const dayStr = options.padDay ? (day + '').padStart(2, '0') : day + ''
    const monthStr = (options.monthPlural ? monthsPlural : monthes)[month]
    const monthShort =
        monthStr.length > 4 ? monthStr.substring(0, 3) + '.' : monthStr

    format = format.replaceAll(/y+/gm, year + '')
    format = format.replaceAll(/d+/gm, dayStr)
    format = format.replaceAll(/m+_str/gm, monthStr)
    format = format.replaceAll(/m+_short/gm, monthShort)
    format = format.replaceAll(/m+/gm, (month + 1 + '').padStart(2, '0'))

    return format
}

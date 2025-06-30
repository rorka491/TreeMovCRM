export const weekDaysShort = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
export const weekDays = [
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'восресенье',
]
export const hoursString = Array.from({ length: 24 }, (_, i) => i + ':00')

export function getMonthDifference(d1: Date, d2: Date) {
    if (d1 > d2) {
        ;[d1, d2] = [d2, d1]
    }

    return (
        (d2.getFullYear() - d1.getFullYear()) * 12 -
        d1.getMonth() +
        d2.getMonth()
    )
}

export const months = [
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

export const monthsPlural = [
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
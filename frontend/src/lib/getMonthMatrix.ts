import { formatDate } from './formatDate'

export function getMonthMatrix(date: Date) {
    const year = date.getFullYear()
    const month = date.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const daysInMonth = lastDay.getDate()
    const startDay = (firstDay.getDay() + 6) % 7 // 0=Пн, ... 6=Вс

    const prevMonthLastDay = new Date(year, month, 0).getDate()
    const matrix: { date: string; week_day: number; current: boolean }[][] = []
    let week: { date: string; week_day: number; current: boolean }[] = []

    // Предыдущий месяц
    for (let i = 0; i < startDay; i++) {
        const day = prevMonthLastDay - startDay + i + 1
        const prevDate = new Date(year, month - 1, day)
        week.push({
            date: formatDate(prevDate),
            week_day: (prevDate.getDay() + 6) % 7,
            current: false,
        })
    }

    // Текущий месяц
    for (let d = 1; d <= daysInMonth; d++) {
        const currDate = new Date(year, month, d)
        week.push({
            date: formatDate(currDate),
            week_day: (currDate.getDay() + 6) % 7,
            current: true,
        })
        if (week.length === 7) {
            matrix.push(week)
            week = []
        }
    }

    // Следующий месяц
    let nextDay = 1
    while (week.length && week.length < 7) {
        const nextDate = new Date(year, month + 1, nextDay++)
        week.push({
            date: formatDate(nextDate),
            week_day: (nextDate.getDay() + 6) % 7,
            current: false,
        })
    }
    if (week.length) matrix.push(week)

    return matrix
}

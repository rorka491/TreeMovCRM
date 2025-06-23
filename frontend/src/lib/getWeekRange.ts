export function getWeekRange(date: Date) {
    const day = date.getDay() === 0 ? 7 : date.getDay()
    const monday = new Date(date)
    monday.setDate(date.getDate() - (day - 1))
    const sunday = new Date(monday)
    sunday.setDate(monday.getDate() + 6)
    const format = (d: Date, withYear = false) =>
        d.toLocaleString('ru-RU', {
            day: 'numeric',
            month: 'long',
            ...(withYear ? { year: 'numeric' } : {}),
        })
    if (
        monday.getMonth() === sunday.getMonth() &&
        monday.getFullYear() === sunday.getFullYear()
    )
        return `${monday.getDate()} - ${sunday.getDate()} ${monday.toLocaleString('ru-RU', { month: 'long', year: 'numeric' })}`
    if (monday.getFullYear() === sunday.getFullYear())
        return `${format(monday)} - ${format(sunday)} ${sunday.getFullYear()}`
    return `${format(monday, true).slice(0, -3)} - ${format(sunday, true).slice(0, -3)}`
}

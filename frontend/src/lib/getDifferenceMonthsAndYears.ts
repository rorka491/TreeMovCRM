export function getDifferenceMonthsAndYears(date1: Date, date2: Date) {
    date1 = new Date(date1)
    date2 = new Date(date2)
    if (date1 > date2) {
        ;[date1, date2] = [date2, date1]
    }

    let years = date2.getFullYear() - date1.getFullYear()
    let m = date2.getMonth() - date1.getMonth()

    if (m < 0 || (m === 0 && date2.getDate() < date1.getDate())) {
        years--
        m += 12
    }

    return [m, years] as const
}

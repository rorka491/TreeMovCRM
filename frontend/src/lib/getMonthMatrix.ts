export function getMonthMatrix(year: number, month: number) {
    const result: { date: Date; currentMonth: boolean }[][] = []
    const firstDay = new Date(year, month, 1)

    const startDayOfWeek = (firstDay.getDay() + 6) % 7
    const startDate = new Date(firstDay)
    startDate.setDate(firstDay.getDate() - startDayOfWeek)

    const totalDays = 6 * 7
    let current = new Date(startDate)

    for (let i = 0; i < totalDays; i++) {
        if (i % 7 === 0) result.push([])
        result[result.length - 1].push({
            date: new Date(current),
            currentMonth: current.getMonth() === month,
        })
        current.setDate(current.getDate() + 1)
    }

    // Удаляем недели, где все дни не входят в текущий месяц
    return result.filter((week) => week.some((day) => day.currentMonth))
}

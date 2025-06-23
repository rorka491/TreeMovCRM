export function getMonthMatrix(year: number, month: number) {
    // Возвращает массив недель, каждая неделя — массив из 7 объектов { date: Date, currentMonth: boolean }
    const result: { date: Date; currentMonth: boolean }[][] = []
    const firstDay = new Date(year, month, 1)

    // Определяем день недели для первого дня месяца (0 - Пн, 6 - Вс)
    const startDayOfWeek = (firstDay.getDay() + 6) % 7

    // Начальная дата для первой недели (может быть из прошлого месяца)
    const startDate = new Date(firstDay)
    startDate.setDate(firstDay.getDate() - startDayOfWeek)

    // Количество дней в матрице (6 недель по 7 дней = 42 дня, чтобы покрыть все случаи)
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

    return result
}

import { useEffect, useState } from 'react'
import { api } from '../../../api'
import { Lesson } from '../../../api/api'
import { formatDate } from '../../../lib/formatDate'
import { getMonthDifference } from '../../../lib/datesHelpers'
import { parseDate } from '../../../lib/parseDate'

// "YYYY-MM"?: Lesson[]
const lessonsCache: { [k: string]: Lesson[] } = {}

async function getLessonsSpan(start: Date, end: Date): Promise<Lesson[]> {
    const startYear = start.getFullYear()
    const startMonth = start.getMonth()

    const monthDiff = getMonthDifference(start, end) + 1

    const promises = Array.from({ length: monthDiff }, (_, i) =>
        preCacheLessons(startMonth + i, startYear)
    )

    const result = await Promise.all(promises)

    return result.flat(1)
}

export async function getLessonsMonth(
    month: number,
    year: number,
    onReal: (l: Lesson[]) => void
): Promise<Lesson[]> {
    const start = new Date(year, month)

    const key = formatDate(start, 'YYYY-MM')

    if (lessonsCache[key]) {
        preCacheLessons(month, year).then(onReal)

        return lessonsCache[key]
    }

    return preCacheLessons(month, year)
}

export async function preCacheLessons(month: number, year: number) {
    const start = new Date(year, month)
    const end = new Date(year, month + 1)

    const key = formatDate(start, 'YYYY-MM')

    const lessons = await api.schedules.getAll({
        startDate: formatDate(start, 'YYYY-MM-DD'),
        endDate: formatDate(end, 'YYYY-MM-DD'),
    })

    return (lessonsCache[key] = lessons.filter(
        (lesson) => parseDate(lesson.date).getMonth() < end.getMonth()
    ))
}

export function useLessons(startDate: Date, endDate: Date) {
    const [lessons, setLessons] = useState<Lesson[]>([])

    useEffect(() => {
        getLessonsSpan(startDate, endDate).then(setLessons)
    }, [])

    return [lessons] as const
}

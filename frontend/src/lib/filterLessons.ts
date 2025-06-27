import { Lesson } from '../components/LessonCard'
import { formatDate } from './formatDate'

export function filterLessons(
    lessons: Lesson[],
    currentDate: Date,
    mode: string
): Lesson[] {
    if (mode === 'by-day') {
        return lessons.filter((l) => l.date === formatDate(currentDate))
    }

    if (mode === 'by-week') {
        const startOfWeek = new Date(currentDate)
        startOfWeek.setDate(currentDate.getDate() - startOfWeek.getDay())
        const endOfWeek = new Date(startOfWeek)
        endOfWeek.setDate(startOfWeek.getDate() + 6)
        return lessons.filter(
            (l) =>
                l.date >= formatDate(startOfWeek) &&
                l.date <= formatDate(endOfWeek)
        )
    }

    if (mode === 'by-month') {
        const startOfMonth = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            1
        )
        const endOfMonth = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth() + 1,
            0
        )
        return lessons.filter(
            (l) =>
                l.date >= formatDate(startOfMonth) &&
                l.date <= formatDate(endOfMonth)
        )
    }

    return []
}

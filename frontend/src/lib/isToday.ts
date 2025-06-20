import { formatDate } from './formatDate'

export function isToday(date: string) {
    const today = new Date()
    return date === formatDate(today)
}

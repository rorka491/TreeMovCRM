import { Lesson } from '../components/LessonCard/LessonCard'

export function isLessonInHour(lesson: Lesson, hour: string, date: string) {
    const [hStart, mStart] = lesson.start_time.split(':').map(Number)
    const [hEnd, mEnd] = lesson.end_time.split(':').map(Number)
    const [h, m] = hour.split(':').map(Number)
    const lessonStart = hStart * 60 + mStart
    const lessonEnd = hEnd * 60 + mEnd
    const time = h * 60 + m
    return time >= lessonStart && time < lessonEnd && date === lesson.date
}

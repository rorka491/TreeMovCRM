import { Lesson } from '../components/LessonCard'
import { parseTime } from './parseTime'

export function getLessonStyle(lesson: Lesson, hourIdx: number, i: number) {
    const startHour = parseTime(lesson.start_time)
    const endHour = parseTime(lesson.end_time)
    const cellHeight = 125

    // Если занятие начинается не в этом часу, не отображаем его
    if (Math.floor(startHour) !== hourIdx) return null

    // top — смещение от начала ячейки (если lesson начинается не ровно в начале)
    const top = (startHour - hourIdx) * cellHeight

    // height — сколько часов (или долей) длится занятие
    const duration = endHour - startHour
    const height = duration * cellHeight

    return {
        top: `${top}px`,
        left: `${i * 180 + (i === 0 ? 0 : 8)}px`,
        height: `${height}px`,
        zIndex: i + 1,
    }
    // return `top-[${top}px] left-[${i * 180 + (i === 0 ? 0 : 8)}px] h-[${height}px] z-[${i + 1}]`
}

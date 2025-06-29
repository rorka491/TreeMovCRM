import { useOutletContext } from 'react-router-dom'
import LessonCard from '../../../components/LessonCard'
import { getLessonStyle } from '../../../lib/getLessonStyle'
import { useEffect, useState } from 'react'
import { filterLessons } from '../../../lib/filterLessons'
import { Lesson } from '../../../api/api'

function ScheduleByDay() {
    const {
        currentDate,
        lessons,
        upsertLesson,
    }: {
        currentDate: Date
        lessons: Lesson[]
        upsertLesson: (newLesson: Lesson) => void
    } = useOutletContext()

    const [dayLessons, setDayLessons] = useState<Lesson[]>([])

    useEffect(() => {
        const filtered = filterLessons(lessons, currentDate, 'by-day')
        // Сортировка по subject.teacher
        filtered.sort((a, b) => {
            const teacherA = a.subject?.teacher || ''
            const teacherB = b.subject?.teacher || ''
            return teacherA.localeCompare(teacherB)
        })
        setDayLessons(filtered)
    }, [lessons, currentDate])

    const [hours, setHours] = useState<number[]>(
        Array.from({ length: 24 }, (_, i) => i)
    )

    useEffect(() => {
        const minHour = Math.max(
            0,
            lessons.reduce(
                (result, lesson) =>
                    Math.min(result, parseInt(lesson.start_time.split(':')[0])),
                24
            ) - 1
        )
        const maxHour = Math.min(
            24,
            lessons.reduce(
                (result, lesson) =>
                    Math.max(result, parseInt(lesson.end_time.split(':')[0])),
                0
            ) + 1
        )

        setHours(
            Array.from({ length: maxHour - minHour }, (_, i) => i + minHour)
        )
    }, [lessons])

    return (
        <tbody>
            {hours.map((hour, hourIdx) => {
                return (
                    <tr
                        key={hourIdx}
                        className="*:h-[125px] *:hover:bg-gray-100 *:border-[#EAECF0] *:bg-white *:transition *:border"
                    >
                        <td className="text-center align-middle border">
                            {hour}:00
                        </td>
                        <td className="relative align-top min-h-[125px]">
                            {dayLessons.map((lesson, i) => {
                                const style = getLessonStyle(lesson, hour, i)
                                if (!style) return null

                                return (
                                    <div
                                        key={lesson.title}
                                        className={`absolute transition-[box-shadow] duration-200`}
                                        style={{
                                            top: style.top,
                                            height: style.height,
                                            zIndex: style.zIndex,
                                            left: style.left,
                                        }}
                                    >
                                        <LessonCard
                                            lesson={lesson}
                                            className="min-w-[180px] w-fit"
                                            onSave={(updatedLesson) =>
                                                upsertLesson(updatedLesson)
                                            }
                                        />
                                    </div>
                                )
                            })}
                        </td>
                    </tr>
                )
            })}
        </tbody>
    )
}

export default ScheduleByDay

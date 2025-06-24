import LessonCard, { Lesson } from '../../../components/LessonCard'
import { useOutletContext } from 'react-router-dom'
import { formatDate } from '../../../lib/formatDate'
import { getLessonStyle } from '../../../lib/getLessonStyle'
import { hours, weekDays } from '../../../lib/calendarConstants'
import { useEffect, useState } from 'react'

function ScheduleByWeek() {
    const {
        currentDate,
        lessons,
        upsertLesson,
    }: {
        currentDate: Date
        lessons: Lesson[]
        upsertLesson: (newLesson: Lesson) => void
    } = useOutletContext()

    const [weekLessons, setWeekLessons] = useState<Lesson[]>([])

    useEffect(() => {
        // Получаем первый и последний день текущей недели
        const startOfWeek = new Date(currentDate)
        startOfWeek.setDate(currentDate.getDate() - startOfWeek.getDay())

        const endOfWeek = new Date(startOfWeek)
        endOfWeek.setDate(startOfWeek.getDate() + 6)

        const data = lessons.filter((l) => {
            return (
                l.date >= formatDate(startOfWeek) &&
                l.date <= formatDate(endOfWeek)
            )
        })
        setWeekLessons(data)
    }, [lessons, currentDate])

    return (
        <tbody>
            {hours.map((hour, rowIdx) => (
                <tr
                    className="*:h-[125px] *:hover:bg-gray-100 *:border-[#EAECF0] *:bg-white *:transition *:border"
                    key={rowIdx}
                >
                    <td className="text-center align-middle border">{hour}</td>

                    {weekDays.map((_, colIdx) => {
                        const cellDate = new Date(currentDate)
                        cellDate.setDate(
                            currentDate.getDate() - cellDate.getDay() + colIdx
                        )
                        const formattedDate = formatDate(cellDate)
                        const dayLessons = weekLessons.filter(
                            (l) => l.date === formattedDate
                        )
                        return (
                            <td
                                key={colIdx}
                                className="relative align-top min-h-[125px]"
                                style={{
                                    position: 'relative',
                                    minHeight: 125,
                                }}
                            >
                                {dayLessons.map((lesson, i) => {
                                    const style = getLessonStyle(
                                        lesson,
                                        rowIdx,
                                        i
                                    )
                                    if (!style) return null

                                    return (
                                        <div
                                            key={lesson.title}
                                            className="absolute transition-[box-shadow] duration-200"
                                            style={{
                                                top: style.top,
                                                height: style.height,
                                                zIndex: style.zIndex + colIdx,
                                                left: i * 8,
                                                width: `calc(100% - ${i * 8}px)`,
                                            }}
                                        >
                                            <LessonCard
                                                lesson={lesson}
                                                onSave={(updatedLesson) =>
                                                    upsertLesson(updatedLesson)
                                                }
                                            />
                                        </div>
                                    )
                                })}
                            </td>
                        )
                    })}
                </tr>
            ))}
        </tbody>
    )
}

export default ScheduleByWeek

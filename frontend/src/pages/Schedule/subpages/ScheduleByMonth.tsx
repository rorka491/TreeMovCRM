import { useNavigate, useOutletContext } from 'react-router-dom'
import LessonCard from '../../../components/LessonCard'
import { formatDate } from '../../../lib/formatDate'
import { useEffect, useState } from 'react'
import { getMonthMatrix } from '../../../lib/getMonthMatrix'
import { PopUpMenu } from '../../../components/PopUpMenu'
import EditLessonPopUp from '../../../components/EditLessonPopUp'
import { filterLessons } from '../../../lib/filterLessons'
import { Lesson } from '../../../api/api'

function ScheduleByMonth() {
    const {
        currentDate,
        lessons,
        upsertLesson,
    }: {
        currentDate: Date
        lessons: Lesson[]
        upsertLesson: (newLesson: Lesson) => void
    } = useOutletContext()
    const navigate = useNavigate()

    const [isAdded, setIsAdded] = useState<string | null>(null)

    const [monthLessons, setMonthLessons] = useState<Lesson[]>([])
    const [currentLesson, setCurrentLesson] = useState<Lesson | null>(null)
    const [isHovered, setIsHovered] = useState<Date | null>(null)
    const [tooltipPos, setTooltipPos] = useState<{
        x: number
        y: number
    } | null>(null)

    useEffect(() => {
        setMonthLessons(filterLessons(lessons, currentDate, 'by-month'))
    }, [lessons, currentDate])

    const monthMatrix = getMonthMatrix(
        currentDate.getFullYear(),
        currentDate.getMonth()
    )

    // Для быстрого поиска занятий по дате
    const lessonsByDate: Record<string, Lesson[]> = {}
    monthLessons.forEach((l) => {
        if (!lessonsByDate[l.date]) lessonsByDate[l.date] = []
        lessonsByDate[l.date].push(l)
    })

    return (
        <tbody>
            {monthMatrix.map((week, weekIdx) => (
                <tr key={weekIdx}>
                    {week.map(({ date, currentMonth }, dayIdx) => {
                        const dayLessons = lessonsByDate[formatDate(date)] || []
                        return (
                            <td
                                onMouseEnter={() =>
                                    dayLessons.length >= 10
                                        ? setIsHovered(date)
                                        : null
                                }
                                onMouseLeave={() =>
                                    dayLessons.length >= 10
                                        ? setIsHovered(null)
                                        : null
                                }
                                onClick={() => {
                                    navigate('/schedule/by-day')
                                    currentDate.setDate(date.getDate())
                                }}
                                key={dayIdx}
                                className={`w-0 min-w-0 overflow-visible max-w-[1px] relative align-top h-[125px] bg-white ${currentMonth ? '' : 'text-[#B3B3B3]'} border border-[#EAECF0] min-h-[125px] transition hover:bg-gray-100 px-[8px] py-[10px]`}
                            >
                                {date && (
                                    <div className="mb-[4px] font-semibold">
                                        {date.getDate()}
                                    </div>
                                )}
                                <div className="flex flex-wrap gap-1">
                                    {dayLessons
                                        .slice(
                                            0,
                                            isHovered?.getTime() ===
                                                date.getTime()
                                                ? Infinity
                                                : Infinity
                                        )
                                        .sort((a, b) => {
                                            const [aHours, aMinutes] = a.start_time.split(':').map(Number)
                                            const [bHours, bMinutes] = b.start_time.split(':').map(Number)
                                            
                                            return (aHours * 60 + aMinutes) - (bHours * 60 + bMinutes)
                                        })
                                        .map((lesson, i) => (
                                            <div
                                                key={lesson.title + i}
                                                className="w-[15px] h-[15px] rounded cursor-pointer inline-block hover:scale-125 transition-transform"
                                                style={{
                                                    background:
                                                        lesson.subject.color
                                                            .color_hex,
                                                }}
                                                onClick={(e) => {
                                                    e.stopPropagation()
                                                    setCurrentLesson(lesson)
                                                    const rect = (
                                                        e.target as HTMLElement
                                                    ).getBoundingClientRect()
                                                    setTooltipPos({
                                                        x:
                                                            rect.left +
                                                            window.scrollX -
                                                            20,
                                                        y:
                                                            rect.top +
                                                            window.scrollY +
                                                            20,
                                                    })
                                                }}
                                            />
                                        ))}
                                </div>
                                {currentLesson && tooltipPos && (
                                    <div
                                        className="fixed z-[9999] w-[180px]"
                                        style={{
                                            top: tooltipPos.y,
                                            left: tooltipPos.x,
                                        }}
                                        onClick={(e) => e.stopPropagation()}
                                    >
                                        <LessonCard
                                            lesson={currentLesson}
                                            isPopUp
                                            onClose={() => {
                                                setCurrentLesson(null)
                                                setTooltipPos(null)
                                            }}
                                            onSave={(updatedLesson) =>
                                                upsertLesson(updatedLesson)
                                            }
                                        />
                                    </div>
                                )}
                            </td>
                        )
                    })}
                </tr>
            ))}
        </tbody>
    )
}

export default ScheduleByMonth

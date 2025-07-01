import { useNavigate, useOutletContext } from 'react-router-dom'
import LessonCard from '../../../components/LessonCard'
import { formatDate } from '../../../lib/formatDate'
import { useEffect, useState } from 'react'
import { getMonthMatrix } from '../../../lib/getMonthMatrix'
import { filterLessons } from '../../../lib/filterLessons'
import { createEmptyLesson, Lesson } from '../../../api/api'
import { weekDaysShort } from '../../../lib/datesHelpers'
import { PopUpMenu } from '../../../components/PopUpMenu'
import EditLessonPopUp from '../../../components/EditLessonPopUp'

function ScheduleByMonth() {
    const {
        currentDate,
        lessons,
    }: {
        currentDate: Date
        lessons: Lesson[]
    } = useOutletContext()
    const navigate = useNavigate()

    const [contextMenuOpen, setContextMenuOpen] = useState<{
        day: number
        week: number
    }>({
        day: -1,
        week: -1,
    })

    const [editLesson, setEditLesson] = useState<Lesson | null>(null)
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
        <div className="relative w-full overflow-y-auto h-[60vh]  special-scroll">
            <PopUpMenu
                open={editLesson !== null}
                onClose={() => setEditLesson(null)}
            >
                <EditLessonPopUp
                    lesson={editLesson!}
                    onSave={() => {
                        setEditLesson(null)
                    }}
                    onClose={() => setEditLesson(null)}
                />
            </PopUpMenu>
            <table className="w-full bg-[#EAECF0] border rounded-xl overflow-hidden">
                <thead className="sticky top-0">
                    <tr>
                        {weekDaysShort.map((d, i) => {
                            const startOfWeek = new Date(currentDate)
                            startOfWeek.setDate(
                                currentDate.getDate() - startOfWeek.getDay()
                            )
                            const dayOfWeek = new Date(startOfWeek)
                            dayOfWeek.setDate(startOfWeek.getDate() + i + 1)
                            return (
                                <th
                                    onClick={() => {
                                        navigate('/schedule/by-day')
                                        currentDate.setDate(
                                            currentDate.getDate() + i
                                        )
                                    }}
                                    key={i}
                                    className="p-2 font-semibold text-center transition bg-[#EDE8FE]"
                                >
                                    {d}
                                </th>
                            )
                        })}
                    </tr>
                </thead>
                <tbody>
                    {monthMatrix.map((week, weekIdx) => (
                        <tr key={weekIdx}>
                            {week.map(({ date, currentMonth }, dayIdx) => {
                                const dayLessons =
                                    lessonsByDate[formatDate(date)] || []
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
                                        onContextMenu={(e) => {
                                            e.preventDefault()
                                            setContextMenuOpen({
                                                week: weekIdx,
                                                day: dayIdx,
                                            })
                                        }}
                                        key={dayIdx}
                                        className={`w-0 min-w-0 overflow-visible max-w-[1px] relative align-top h-[125px] bg-white ${currentMonth ? '' : 'text-[#B3B3B3]'} border border-[#EAECF0] min-h-[125px] transition hover:bg-gray-100 px-[8px] py-[10px]`}
                                    >
                                        <PopUpMenu
                                            open={
                                                contextMenuOpen.week ===
                                                    weekIdx &&
                                                contextMenuOpen.day === dayIdx
                                            }
                                            onClose={() =>
                                                setContextMenuOpen({
                                                    week: -1,
                                                    day: -1,
                                                })
                                            }
                                            followMouse
                                            className="flex flex-col gap-2 bg-white rounded-xl border-1"
                                        >
                                            <button
                                                onClick={(e) => {
                                                    e.preventDefault()
                                                    e.stopPropagation()
                                                    setEditLesson(
                                                        createEmptyLesson()
                                                    )
                                                    setContextMenuOpen({
                                                        week: -1,
                                                        day: -1,
                                                    })
                                                }}
                                                className="bg-white min-w-[140px] hover:bg-gray-100 px-3 py-2"
                                            >
                                                Создать урок
                                            </button>

                                            {dayLessons.length > 0 && (
                                                <button className="bg-white min-w-[140px] hover:bg-gray-100 px-3 py-2">
                                                    Удалить
                                                </button>
                                            )}
                                        </PopUpMenu>
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
                                                    const [aHours, aMinutes] =
                                                        a.start_time
                                                            .split(':')
                                                            .map(Number)
                                                    const [bHours, bMinutes] =
                                                        b.start_time
                                                            .split(':')
                                                            .map(Number)

                                                    return (
                                                        aHours * 60 +
                                                        aMinutes -
                                                        (bHours * 60 + bMinutes)
                                                    )
                                                })
                                                .map((lesson, i) => (
                                                    <div
                                                        key={lesson.title + i}
                                                        className="w-[15px] h-[15px] rounded cursor-pointer inline-block hover:scale-125 transition-transform"
                                                        style={{
                                                            background:
                                                                lesson.subject
                                                                    .color
                                                                    .color_hex,
                                                        }}
                                                        onClick={(e) => {
                                                            e.stopPropagation()
                                                            setCurrentLesson(
                                                                lesson
                                                            )
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
                                                onClick={(e) =>
                                                    e.stopPropagation()
                                                }
                                            >
                                                <LessonCard
                                                    lesson={currentLesson}
                                                    isPopUp
                                                    onClose={() => {
                                                        setCurrentLesson(null)
                                                        setTooltipPos(null)
                                                    }}
                                                />
                                            </div>
                                        )}
                                    </td>
                                )
                            })}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default ScheduleByMonth

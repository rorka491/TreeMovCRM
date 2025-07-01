import LessonCard from '../../../components/LessonCard'
import { useNavigate, useOutletContext } from 'react-router-dom'
import { formatDate } from '../../../lib/formatDate'
import { getLessonStyle } from '../../../lib/getLessonStyle'
import { weekDaysShort } from '../../../lib/datesHelpers'
import { useEffect, useState } from 'react'
import { filterLessons } from '../../../lib/filterLessons'
import { createEmptyLesson, Lesson } from '../../../api/api'
import { PopUpMenu } from '../../../components/PopUpMenu'
import EditLessonPopUp from '../../../components/EditLessonPopUp'

function ScheduleByWeek() {
    const {
        currentDate,
        lessons,
    }: {
        currentDate: Date
        lessons: Lesson[]
    } = useOutletContext()
    const navigate = useNavigate()

    const [editLesson, setEditLesson] = useState<Lesson | null>(null)
    const [weekLessons, setWeekLessons] = useState<Lesson[]>([])
    const [contextMenuOpen, setContextMenuOpen] = useState<{
        row: number
        col: number
    }>({
        row: -1,
        col: -1,
    })

    useEffect(() => {
        setWeekLessons(filterLessons(lessons, currentDate, 'by-week'))
    }, [lessons, currentDate])

    const [hours, setHours] = useState<number[]>(
        Array.from({ length: 24 }, (_, i) => i)
    )

    useEffect(() => {
        const minHour = Math.max(
            0,
            lessons.length > 0
                ? lessons.reduce(
                      (result, lesson) =>
                          Math.min(
                              result,
                              parseInt(lesson.start_time.split(':')[0])
                          ),
                      24
                  ) - 2
                : 0
        )
        const maxHour = Math.min(
            24,
            lessons.length > 0
                ? lessons.reduce(
                      (result, lesson) =>
                          Math.max(
                              result,
                              parseInt(lesson.end_time.split(':')[0])
                          ),
                      0
                  ) + 2
                : 24
        )

        setHours(
            Array.from({ length: maxHour - minHour }, (_, i) => i + minHour)
        )
    }, [lessons])

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
                        <th className="w-24 font-normal bg-white">Часы</th>
                        {weekDaysShort.map((d, i) => {
                            const startOfWeek = new Date(currentDate)
                            startOfWeek.setDate(
                                currentDate.getDate() - startOfWeek.getDay()
                            )
                            const dayOfWeek = new Date(startOfWeek)
                            dayOfWeek.setDate(startOfWeek.getDate() + i + 1)
                            const dayNum = dayOfWeek.getDate()
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
                                    {d} {dayNum}
                                </th>
                            )
                        })}
                    </tr>
                </thead>
                <tbody>
                    {hours.map((hour, rowIdx) => (
                        <tr
                            className="*:h-[125px] *:hover:bg-gray-100 *:border-[#EAECF0] *:bg-white *:transition *:border"
                            key={rowIdx}
                        >
                            <td className="text-center align-middle border">
                                {hour}:00
                            </td>

                            {weekDaysShort.map((_, colIdx) => {
                                const cellDate = new Date(currentDate)
                                cellDate.setDate(
                                    currentDate.getDate() -
                                        cellDate.getDay() +
                                        colIdx
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
                                        onContextMenu={(e) => {
                                            e.preventDefault()

                                            setContextMenuOpen({
                                                row: rowIdx,
                                                col: colIdx,
                                            })
                                        }}
                                    >
                                        <PopUpMenu
                                            open={
                                                contextMenuOpen.col ===
                                                    colIdx &&
                                                contextMenuOpen.row === rowIdx
                                            }
                                            onClose={() =>
                                                setContextMenuOpen({
                                                    row: -1,
                                                    col: -1,
                                                })
                                            }
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
                                                        col: -1,
                                                        row: -1,
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
                                        {dayLessons.map((lesson, i) => {
                                            const style = getLessonStyle(
                                                lesson,
                                                hour,
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
                                                        zIndex:
                                                            style.zIndex +
                                                            colIdx,
                                                        left: i * 8,
                                                        width: `calc(100% - ${i * 8}px)`,
                                                    }}
                                                >
                                                    <LessonCard
                                                        lesson={lesson}
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
            </table>
        </div>
    )
}

export default ScheduleByWeek

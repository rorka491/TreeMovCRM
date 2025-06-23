import { useNavigate, useOutletContext } from 'react-router-dom'
import LessonCard, { Lesson } from '../../../components/LessonCard/LessonCard'
import { formatDate } from '../../../lib/formatDate'
import { useState } from 'react'
import { getMonthMatrix } from '../../../lib/getMonthMatrix'

const WEEKDAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

const lessons: Lesson[] = [
    {
        title: 'Математика',
        start_time: '09:00:00',
        end_time: '10:30:00',
        date: '30.06.2025',
        teacher: 1,
        week_day: 1,
        classroom: {
            title: '101',
            floor: 1,
            building: 1,
        },
        group: 101,
        subject: {
            name: 'Алгебра',
            teacher: 'Иванов И.И.',
            color: '#3498db',
        },
        is_canceled: false,
        is_completed: true,
        lesson: 1,
    },
    {
        title: 'Физика',
        start_time: '10:45:00',
        end_time: '12:15:00',
        date: '25.06.2025',
        teacher: 2,
        week_day: 3,
        classroom: {
            title: '203',
            floor: 2,
            building: 1,
        },
        group: 101,
        subject: {
            name: 'Механика',
            teacher: 'Петров П.П.',
            color: '#e74c3c',
        },
        is_canceled: false,
        is_completed: true,
        lesson: 2,
    },
    {
        title: 'Химия',
        start_time: '13:00:00',
        end_time: '14:30:00',
        date: '20.06.2025',
        teacher: 3,
        week_day: 5,
        classroom: {
            title: 'Лаб. 5',
            floor: 3,
            building: 2,
        },
        group: 101,
        subject: {
            name: 'Органическая химия',
            teacher: 'Сидорова С.С.',
            color: '#2ecc71',
        },
        is_canceled: true,
        is_completed: false,
        lesson: 3,
    },
    {
        title: 'Литература',
        start_time: '15:00:00',
        end_time: '16:30:00',
        date: '20.06.2025',
        teacher: 4,
        week_day: 5,
        classroom: {
            title: '305',
            floor: 3,
            building: 1,
        },
        group: 102,
        subject: {
            name: 'Русская литература',
            teacher: 'Кузнецова К.К.',
            color: '#f39c12',
        },
        is_canceled: false,
        is_completed: false,
        lesson: 4,
    },
    {
        title: 'Физкультура',
        start_time: '09:00:00',
        end_time: '10:30:00',
        date: '23.06.2025',
        teacher: 5,
        week_day: 1,
        classroom: {
            title: 'Спортзал',
            floor: 1,
            building: 3,
        },
        group: 102,
        subject: {
            name: 'Баскетбол',
            teacher: 'Смирнов С.С.',
            color: '#9b59b6',
        },
        is_canceled: false,
        is_completed: false,
        lesson: 5,
    },
    {
        title: 'Информатика',
        start_time: '11:00:00',
        end_time: '12:30:00',
        date: '23.06.2025',
        teacher: 6,
        week_day: 1,
        classroom: {
            title: 'Комп. класс 1',
            floor: 2,
            building: 2,
        },
        group: 103,
        subject: {
            name: 'Программирование',
            teacher: 'Алексеев А.А.',
            color: '#1abc9c',
        },
        is_canceled: false,
        is_completed: false,
        lesson: 6,
    },
    {
        title: 'История',
        start_time: '14:00:00',
        end_time: '15:30:00',
        date: '12.06.2025',
        teacher: 7,
        week_day: 4,
        classroom: {
            title: '207',
            floor: 2,
            building: 1,
        },
        group: 101,
        subject: {
            name: 'Всемирная история',
            teacher: 'Николаева Н.Н.',
            color: '#d35400',
        },
        is_canceled: false,
        is_completed: false,
        lesson: 7,
    },
]

function ScheduleByMonth() {
    let currentDate: Date = useOutletContext()
    const navigate = useNavigate()

    const [hoveredLesson, setHoveredLesson] = useState<Lesson | null>(null)
    const [tooltipPos, setTooltipPos] = useState<{
        x: number
        y: number
    } | null>(null)

    const year = currentDate.getFullYear()
    const month = currentDate.getMonth()
    const monthMatrix = getMonthMatrix(year, month)

    // Для быстрого поиска занятий по дате
    const lessonsByDate: Record<string, Lesson[]> = {}
    lessons.forEach((l) => {
        if (!lessonsByDate[l.date]) lessonsByDate[l.date] = []
        lessonsByDate[l.date].push(l)
    })

    return (
        <section className="flex flex-col w-full h-full gap-4 bg-[#F7F7FA] min-h-screen">
            <div className="w-full overflow-y-scroll h-[60vh] special-scroll">
                <table className="w-full bg-[#EAECF0] border rounded-[12.5px] overflow-hidden">
                    <thead>
                        <tr>
                            {WEEKDAYS.map((d, i) => (
                                <th
                                    key={i}
                                    className="font-semibold border align-top text-center p-[8px] border-[#EAECF0] bg-[#A78BFA33] select-none"
                                >
                                    {d}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {monthMatrix.map((week, weekIdx) => (
                            <tr key={weekIdx}>
                                {week.map(({ date, currentMonth }, dayIdx) => {
                                    const formatted = formatDate(date)

                                    const dayLessons =
                                        lessonsByDate[formatted] || []
                                    return (
                                        <td
                                            onClick={() => {
                                                navigate('/schedule/by-day')
                                                currentDate.setDate(
                                                    date.getDate()
                                                )
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
                                                {dayLessons.map((lesson, i) => (
                                                    <div
                                                        key={lesson.title + i}
                                                        className="w-[15px] h-[15px] rounded cursor-pointer inline-block"
                                                        style={{
                                                            background:
                                                                lesson.subject
                                                                    .color,
                                                        }}
                                                        onMouseEnter={(e) => {
                                                            setHoveredLesson(
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
                                                        onMouseLeave={() => {
                                                            setHoveredLesson(
                                                                null
                                                            )
                                                            setTooltipPos(null)
                                                        }}
                                                    />
                                                ))}
                                            </div>
                                            {hoveredLesson && tooltipPos && (
                                                <div
                                                    className="fixed z-[9999] pointer-events-none w-max max-w-[300px]"
                                                    style={{
                                                        top: tooltipPos.y,
                                                        left: tooltipPos.x,
                                                    }}
                                                >
                                                    <LessonCard
                                                        lesson={hoveredLesson}
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
        </section>
    )
}

export default ScheduleByMonth

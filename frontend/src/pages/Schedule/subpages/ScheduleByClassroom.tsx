import { useState, useEffect } from 'react'
import { api } from '../../../api'

const DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

function ScheduleByClassroom() {
    const [data, setData] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        ;(async () => {
            const data = await api.schedules.getClassroomsRequest()
            setData(data)
        })()
    }, [])

    const getDayOfWeek = (dateStr) => {
        const date = new Date(dateStr)
        const day = date.getDay()
        return day === 0 ? 6 : day - 1
    }

    // Группируем расписание по lesson (пара) и дню недели
    const groupByLessonAndDay = (schedules) => {
        const result = {}
        schedules.forEach((s) => {
            const lesson = s.lesson
            const dayIndex = getDayOfWeek(s.date)
            if (!result[lesson]) result[lesson] = {}
            result[lesson][dayIndex] = s
        })
        return result
    }

    if (loading) return <div>Загрузка...</div>
    if (error) return <div>Ошибка: {error}</div>

    return (
        <div>
            {data.length === 0 && <div>Данные не найдены</div>}
            {data.map(({ classroom, schedules }) => {
                const grid = groupByLessonAndDay(schedules)
                const lessons = Object.keys(grid).sort((a, b) => +a - +b)

                return (
                    <div key={classroom} className="mb-12">
                        <h2 className="mb-4 text-xl font-semibold">
                            Аудитория: {classroom}
                        </h2>
                        <table className="w-full text-sm border border-collapse table-auto">
                            <thead>
                                <tr>
                                    <th className="px-2 py-1 border">Пара</th>
                                    {DAYS.map((day, i) => (
                                        <th
                                            key={i}
                                            className="px-2 py-1 border"
                                        >
                                            {day}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {lessons.map((lesson) => (
                                    <tr key={lesson}>
                                        <td className="px-2 py-1 font-medium border">
                                            {lesson}
                                        </td>
                                        {DAYS.map((_, dayIdx) => {
                                            const cell = grid[lesson][dayIdx]
                                            return (
                                                <td
                                                    key={dayIdx}
                                                    className="px-2 py-1 align-top border"
                                                >
                                                    {cell ? (
                                                        <>
                                                            <strong>
                                                                {cell.title}
                                                            </strong>
                                                            <br />
                                                            Преподаватель:{' '}
                                                            {cell.teacher}
                                                            <br />
                                                            Время:{' '}
                                                            {
                                                                cell.start_time
                                                            } — {cell.end_time}
                                                            <br />
                                                        </>
                                                    ) : (
                                                        '-'
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
            })}
        </div>
    )
}

export default ScheduleByClassroom

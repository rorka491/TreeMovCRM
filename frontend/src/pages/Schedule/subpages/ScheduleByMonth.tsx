import { useState } from 'react'
import { getMonthMatrix } from '../../../lib/getMonthMatrix'
import { isToday } from '../../../lib/isToday'
import { PopUpMenu } from '../../../components/PopUpMenu'
import { parseDate } from '../../../lib/parseDate'
import { useOutletContext } from 'react-router-dom'

const WEEKDAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

const testSchedules = [
    {
        title: 'Математические занятия',
        start_time: '09:00:00',
        end_time: '10:30:00',
        date: '15.06.2025',
        teacher: 1,
        week_day: 6,
        classroom: {
            title: '101',
            floor: 6,
            building: 2,
        },
        group: 5,
        subject: {
            name: 'Математика',
            teacher: 'Роман',
            color: '#F00FF0',
        },
        is_canceled: false,
        is_completed: true,
        lesson: 1,
    },
    {
        title: 'Математические занятия',
        start_time: '09:00:00',
        end_time: '10:30:00',
        date: '30.06.2025',
        teacher: 1,
        week_day: 6,
        classroom: {
            title: '101',
            floor: 6,
            building: 2,
        },
        group: 5,
        subject: {
            name: 'Математика',
            teacher: 'Роман',
            color: '#F00FF0',
        },
        is_canceled: false,
        is_completed: true,
        lesson: 1,
    },
    {
        title: 'Математические занятия',
        start_time: '09:00:00',
        end_time: '10:30:00',
        date: '20.06.2025',
        teacher: 1,
        week_day: 6,
        classroom: {
            title: '101',
            floor: 6,
            building: 2,
        },
        group: 5,
        subject: {
            name: 'Математика',
            teacher: 'Роман',
            color: '#F00FF0',
        },
        is_canceled: false,
        is_completed: true,
        lesson: 1,
    },
]

function mergeSchedulesToMatrix(matrix: any[][], schedules: any[]) {
    return matrix.map((week) =>
        week.map((cell) =>
            schedules.map((el) =>
                el.date === cell.date ? { ...cell, ...el } : { ...cell }
            )
        )
    )
}

function ScheduleByMonth() {
    const currentDate: Date = useOutletContext()
    const matrix = mergeSchedulesToMatrix(
        getMonthMatrix(currentDate),
        testSchedules
    )
    const [popupOpen, setPopupOpen] = useState<string | number>(-1)

    return (
        <section className="w-full h-full grid grid-rows-[max-content_1fr] gap-y-[16px]">
            <div className="w-full overflow-y-scroll h-[60vh] special-scroll">
                <table className="w-full bg-[#EAECF0] border rounded-[12.5px] overflow-hidden">
                    <tr>
                        {WEEKDAYS.map((d, i) => (
                            <th
                                key={i}
                                className={`font-semibold border align-top text-center transition p-[8px] hover:bg-gray-100 border-[#EAECF0] bg-white cursor-pointer select-none`}
                            >
                                {d}
                            </th>
                        ))}
                    </tr>
                    <tbody>
                        {matrix.map((week, i) => (
                            <tr key={i}>
                                {week.map((el, j) => {
                                    const { date, current, week_day } = el[0]
                                    return (
                                        <td
                                            key={j}
                                            onMouseUp={() => setPopupOpen(date)}
                                            className={`h-[125px] border align-top text-center transition p-[8px] hover:bg-gray-100
                                        ${
                                            current
                                                ? isToday(date)
                                                    ? 'border-[#7816DB] border-[2px] border-dashed bg-[#f3a4ea82]'
                                                    : 'border-[#EAECF0] bg-white'
                                                : 'bg-[#EAECF0]'
                                        }
                                        cursor-pointer select-none`}
                                        >
                                            <span className="flex items-center justify-center mx-auto mt-[2px] mb-[10px]">
                                                {`${WEEKDAYS[week_day]} ${parseDate(date).getDate()}`}
                                            </span>
                                            <li className="grid grid-flow-col grid-cols-[repeat(auto-fill,15px)] gap-[4px] flex-wrap">
                                                {[1, 2, 3, 4].map((el, i) => {
                                                    if (i < 5) {
                                                        return (
                                                            <ul
                                                                key={i}
                                                                className={`flex w-[15px] h-[15px] rounded-[5px]`}
                                                                style={{
                                                                    background:
                                                                        // COLORS[
                                                                        //     el
                                                                        // ],
                                                                        'black',
                                                                }}
                                                            ></ul>
                                                        )
                                                    } else if (i === 5) {
                                                        return (
                                                            <div>
                                                                {'+' + (10 - 5)}
                                                            </div>
                                                        )
                                                    } else return null
                                                })}
                                            </li>
                                            <PopUpMenu
                                                open={popupOpen === date}
                                                onClose={() => setPopupOpen(-1)}
                                            >
                                                <div className="bg-black h-100 w-100"></div>
                                            </PopUpMenu>
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

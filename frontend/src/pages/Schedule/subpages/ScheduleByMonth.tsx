import { useState } from 'react'
import { getMonthMatrix } from '../../../lib/getMonthMatrix'
import { isToday } from '../../../lib/isToday'
import { PopUpMenu } from '../../../components/PopUpMenu'
import { parseDate } from '../../../lib/parseDate'
import { useOutletContext } from 'react-router-dom'
import { Lesson } from '../../../components/LessonCard/LessonCard'

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
    const currentDate: Date = useOutletContext()
    const matrix = getMonthMatrix(currentDate)

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
                                    const { date, current, week_day } = el
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
                                            <span className="flex mt-[2px] mb-[10px]">
                                                {parseDate(date).getDate()}
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

import { useState } from 'react'
import { PopUpMenu } from '../../../components/PopUpMenu'

const WEEKDAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
const HOURS = [
    '8:00',
    '9:00',
    '10:00',
    '11:00',
    '12:00',
    '13:00',
    '14:00',
    '15:00',
    '16:00',
    '17:00',
    '18:00',
    '19:00',
    '20:00',
    '21:00',
    '22:00',
    '23:00',
]
// Пример расписания для недели
const weekSchedules = [
    {
        title: 'История',
        teacher: 'Иосиф Жернов',
        color: '#FFD600',
        date: '2024-06-10',
        start: '12:30',
        end: '13:30',
        room: '205',
        groups: ['5, 6, 21'],
        day: 0,
        timeIndex: 3,
    },
    {
        title: 'Астрономия',
        teacher: 'Антон Журавлев, Артемий Грек',
        color: '#00C2C2',
        date: '2024-06-11',
        start: '10:00',
        end: '12:10',
        room: '32',
        groups: ['1, 7, 21'],
        day: 1,
        timeIndex: 1,
    },
    {
        title: 'Танцы',
        teacher: 'Борис Семенюк',
        color: '#4D8CFF',
        date: '2024-06-12',
        start: '12:45',
        end: '14:00',
        room: '437',
        groups: ['21'],
        day: 2,
        timeIndex: 4,
    },
    {
        title: 'Математика',
        teacher: 'Иосиф Хромов',
        color: '#FFB3DE',
        date: '2024-06-14',
        start: '12:30',
        end: '13:30',
        room: '205',
        groups: ['21, 14'],
        day: 4,
        timeIndex: 3,
    },
]

function SheduleByWeek() {
    const [popupOpen, setPopupOpen] = useState<{
        row: null | number
        col: null | number
    }>({ row: null, col: null })

    return (
        <section className="flex flex-col w-full h-full gap-4 bg-[#F7F7FA] min-h-screen">
            <div className="w-full overflow-y-scroll h-[60vh] special-scroll">
                <table className="w-full bg-[#EAECF0] border rounded-[12.5px] overflow-hidden">
                    <thead>
                        <tr>
                            <th className="text-base font-normal w-[100px] border-[#EAECF0] bg-white">
                                Часы
                            </th>
                            {WEEKDAYS.map((d, i) => (
                                <th
                                    onMouseEnter={() =>
                                        setPopupOpen({ row: null, col: i })
                                    }
                                    key={i}
                                    className={`font-semibold border align-top text-center transition p-[8px] hover:bg-gray-100 ${
                                        i === popupOpen.col
                                            ? 'bg-[#A78BFA33]'
                                            : 'border-[#EAECF0] bg-white'
                                    }
                                                                        cursor-pointer select-none`}
                                >
                                    {d}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {HOURS.map((hour, rowIdx) => (
                            <tr key={rowIdx}>
                                <td
                                    onMouseEnter={() =>
                                        setPopupOpen({ row: rowIdx, col: null })
                                    }
                                    className={`h-[125px] border align-top text-center transition p-[8px] hover:bg-gray-100
                                                                        ${
                                                                            rowIdx ===
                                                                            popupOpen.row
                                                                                ? 'bg-[#A78BFA33]'
                                                                                : 'border-[#EAECF0] bg-white'
                                                                        }
                                                                        cursor-pointer select-none`}
                                >
                                    {hour}
                                </td>
                                {WEEKDAYS.map((_, colIdx) => {
                                    const lesson = weekSchedules.find(
                                        (l) =>
                                            l.day === colIdx &&
                                            l.timeIndex === rowIdx
                                    )
                                    return (
                                        <td
                                            key={colIdx}
                                            className={`h-[125px] border align-top text-center transition p-[8px] hover:bg-gray-100
                                                                        ${
                                                                            rowIdx ===
                                                                                popupOpen.row ||
                                                                            colIdx ===
                                                                                popupOpen.col
                                                                                ? 'bg-[#A78BFA33]'
                                                                                : 'border-[#EAECF0] bg-white'
                                                                        }
                                                                        cursor-pointer select-none`}
                                            onMouseEnter={() =>
                                                setPopupOpen({
                                                    row: rowIdx,
                                                    col: colIdx,
                                                })
                                            }
                                        >
                                            {lesson && (
                                                <div
                                                    className="absolute left-1 top-1 w-[220px] px-3 py-2 text-left border rounded-xl shadow-sm cursor-pointer bg-white"
                                                    style={{
                                                        borderColor:
                                                            lesson.color,
                                                        boxShadow:
                                                            '0 2px 8px #0001',
                                                    }}
                                                >
                                                    <div className="flex items-center gap-2 mb-1">
                                                        <span
                                                            className="inline-block w-3 h-3 rounded-full"
                                                            style={{
                                                                background:
                                                                    lesson.color,
                                                            }}
                                                        ></span>
                                                        <span className="font-semibold">
                                                            {lesson.title}
                                                        </span>
                                                    </div>
                                                    <div className="text-xs text-gray-700">
                                                        {lesson.teacher}
                                                    </div>
                                                    <div className="text-xs text-gray-500">
                                                        Каб. {lesson.room}
                                                    </div>
                                                    <div className="text-xs text-gray-500">
                                                        {lesson.groups.join(
                                                            ', '
                                                        )}
                                                    </div>
                                                    <div className="text-xs text-gray-400">
                                                        {lesson.start}–
                                                        {lesson.end}
                                                    </div>
                                                </div>
                                            )}
                                            {/* PopUpMenu пример */}
                                            {lesson &&
                                                popupOpen.row === rowIdx &&
                                                popupOpen.col === colIdx && (
                                                    <PopUpMenu
                                                        open={true}
                                                        onClose={() =>
                                                            setPopupOpen({
                                                                row: null,
                                                                col: null,
                                                            })
                                                        }
                                                    >
                                                        <div className="p-4 bg-white rounded shadow">
                                                            Детали занятия
                                                        </div>
                                                    </PopUpMenu>
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

export default SheduleByWeek

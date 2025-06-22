import { useState } from 'react'
import Select from '../Select'
import { useMatch, useNavigate } from 'react-router-dom'

const VIEW_OPTIONS = [
    { value: 'День', key: 'by-day' },
    { value: 'Неделя', key: 'by-week' },
    { value: 'Месяц', key: 'by-month' },
]

const RADIO_OPTIONS = [
    {
        value: 'list',
        icon: (
            <>
                <rect
                    x="5"
                    y="6"
                    width="10"
                    height="1.5"
                    rx=".75"
                    fill="#BDBDBD"
                />
                <rect
                    x="5"
                    y="9.25"
                    width="10"
                    height="1.5"
                    rx=".75"
                    fill="#BDBDBD"
                />
                <rect
                    x="5"
                    y="12.5"
                    width="10"
                    height="1.5"
                    rx=".75"
                    fill="#BDBDBD"
                />
            </>
        ),
    },
    {
        value: 'calendar',
        icon: (
            <>
                <rect
                    x="3"
                    y="5"
                    width="14"
                    height="12"
                    rx="2"
                    fill="#E1D8FB"
                    stroke="#BDBDBD"
                />
                <rect x="6" y="9" width="2" height="2" rx="1" fill="#BDBDBD" />
                <rect x="10" y="9" width="2" height="2" rx="1" fill="#BDBDBD" />
                <rect x="14" y="9" width="2" height="2" rx="1" fill="#BDBDBD" />
                <rect x="6" y="13" width="2" height="2" rx="1" fill="#BDBDBD" />
                <rect
                    x="10"
                    y="13"
                    width="2"
                    height="2"
                    rx="1"
                    fill="#BDBDBD"
                />
                <rect
                    x="14"
                    y="13"
                    width="2"
                    height="2"
                    rx="1"
                    fill="#BDBDBD"
                />
                <rect x="7" y="3" width="1" height="3" rx=".5" fill="#BDBDBD" />
                <rect
                    x="12"
                    y="3"
                    width="1"
                    height="3"
                    rx=".5"
                    fill="#BDBDBD"
                />
            </>
        ),
    },
]

function getWeekRange(date: Date) {
    // Monday as first day of week
    const day = date.getDay() === 0 ? 7 : date.getDay()
    const monday = new Date(date)
    monday.setDate(date.getDate() - (day - 1))
    const sunday = new Date(monday)
    sunday.setDate(monday.getDate() + 6)

    // Форматирование для разных случаев
    const format = (d: Date, withYear = false) =>
        d.toLocaleString('ru-RU', {
            day: 'numeric',
            month: 'long',
            ...(withYear ? { year: 'numeric' } : {}),
        })

    // Одна неделя в пределах одного месяца и года
    if (
        monday.getMonth() === sunday.getMonth() &&
        monday.getFullYear() === sunday.getFullYear()
    ) {
        return (
            `${monday.getDate()} - ${sunday.getDate()} ` +
            monday.toLocaleString('ru-RU', {
                month: 'long',
                year: 'numeric',
            })
        )
    }

    // Неделя в пределах одного года, но разные месяцы
    if (monday.getFullYear() === sunday.getFullYear()) {
        return `${format(monday)} - ${format(sunday)} ${sunday.getFullYear()}`
    }

    // Неделя на стыке годов
    return `${format(monday, true).slice(0, -3)} - ${format(sunday, true).slice(0, -3)}`
}

function CalendarBar({
    currentDate,
    setCurrentDate,
}: {
    currentDate: Date
    setCurrentDate: React.Dispatch<React.SetStateAction<Date>>
}) {
    const [selected, setSelected] = useState(VIEW_OPTIONS[2])

    const match = useMatch('/:any/:lastPart/*')
    const activeSection = match?.params?.lastPart || 'by-month'
    const navigate = useNavigate()

    const month = currentDate.getMonth()
    const date = currentDate.getDate()
    const dayMonthYear = currentDate.toLocaleString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    })
    const monthYear = currentDate.toLocaleString('ru-RU', {
        month: 'long',
        year: 'numeric',
    })

    const changeDate = (amount: number, type: 'day' | 'week' | 'month') => {
        const newDate = new Date(currentDate)
        if (type === 'day') newDate.setDate(date + amount)
        else if (type === 'week') newDate.setDate(date + amount * 7)
        else newDate.setMonth(month + amount, 1)
        setCurrentDate(newDate)
    }

    const getViewType = () => {
        if (activeSection === 'by-day') return 'day'
        if (activeSection === 'by-week') return 'week'
        return 'month'
    }

    return (
        <div className="flex items-center justify-between">
            <div className="flex gap-[6px] items-center *:cursor-pointer">
                <button
                    onClick={() => changeDate(-1, getViewType())}
                    className="grid place-items-center w-[20px] h-[20px] border-[#616161] border rounded-full"
                    aria-label="Предыдущий период"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-[10px]"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fillRule="evenodd"
                            d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                            clipRule="evenodd"
                        />
                    </svg>
                </button>
                <button
                    onClick={() => changeDate(1, getViewType())}
                    className="grid place-items-center w-[20px] h-[20px] border-[#616161] border rounded-full"
                    aria-label="Следующий период"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-[10px]"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fillRule="evenodd"
                            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                            clipRule="evenodd"
                        />
                    </svg>
                </button>
                <button
                    className="font-semibold"
                    onClick={() => setCurrentDate(new Date())}
                >
                    {activeSection === 'by-month'
                        ? monthYear[0].toUpperCase() +
                          monthYear.slice(1).slice(0, -3)
                        : activeSection === 'by-week'
                          ? getWeekRange(currentDate)
                          : dayMonthYear[0].toUpperCase() +
                            dayMonthYear.slice(1).slice(0, -3)}
                </button>
            </div>
            <div className="flex items-center gap-2">
                <Select
                    options={VIEW_OPTIONS}
                    className="h-[26px]"
                    placeholder={
                        VIEW_OPTIONS.find((v) => v.key === activeSection)
                            ?.value || 'Месяц'
                    }
                    onSelected={(newSelected) => {
                        navigate('/schedule/' + newSelected.key)
                        setSelected(newSelected)
                    }}
                />
                <div className="flex gap-2">
                    {RADIO_OPTIONS.map((opt) => (
                        <label key={opt.value}>
                            <input
                                type="radio"
                                name="calendar-view"
                                className="hidden peer"
                                value={opt.value}
                            />
                            <span className="w-[36px] h-[26px] rounded-full border border-[#E0E0E0] flex items-center justify-center peer-checked:bg-[#F4F2FF] cursor-pointer">
                                <svg
                                    width="20"
                                    height="20"
                                    fill="none"
                                    viewBox="0 0 20 20"
                                >
                                    {opt.icon}
                                </svg>
                            </span>
                        </label>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default CalendarBar

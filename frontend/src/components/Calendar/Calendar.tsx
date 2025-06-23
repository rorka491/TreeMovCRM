import { useEffect, useState } from 'react'
import { getMonthMatrix } from '../../lib/getMonthMatrix'

interface CalendarProps {
    value: Date
    onChange: (date: Date) => void
    minDate?: Date
    maxDate?: Date
    renderDay?: (
        date: Date,
        isCurrentMonth: boolean,
        isSelected: boolean
    ) => React.ReactNode
}

const WEEKDAYS = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']

function Calendar({
    value,
    onChange,
    minDate,
    maxDate,
    renderDay,
}: CalendarProps) {
    const [current, setCurrent] = useState<Date>(new Date(value))

    useEffect(() => {
        setCurrent(new Date(value))
    }, [value])

    const year = current.getFullYear()
    const month = current.getMonth()
    const matrix = getMonthMatrix(year, month)

    const isSameDay = (d1: Date, d2: Date) =>
        d1.getFullYear() === d2.getFullYear() &&
        d1.getMonth() === d2.getMonth() &&
        d1.getDate() === d2.getDate()

    const canSelect = (date: Date) => {
        if (minDate && date < minDate) return false
        if (maxDate && date > maxDate) return false
        return true
    }

    return (
        <div className="bg-white rounded-xl p-4 w-[320px] shadow">
            <div className="flex items-center justify-between px-2 mb-2">
                <button
                    className="px-2 text-xl text-gray-400 hover:text-gray-700"
                    onClick={() => setCurrent(new Date(year, month - 1, 1))}
                    aria-label="Предыдущий месяц"
                >
                    &#60;
                </button>
                <span className="text-lg font-semibold select-none">
                    {current
                        .toLocaleString('ru-RU', {
                            month: 'long',
                            year: 'numeric',
                        })
                        .toUpperCase()}
                </span>
                <button
                    className="px-2 text-xl text-gray-400 hover:text-gray-700"
                    onClick={() => setCurrent(new Date(year, month + 1, 1))}
                    aria-label="Следующий месяц"
                >
                    &#62;
                </button>
            </div>
            <table className="w-full text-center select-none">
                <thead>
                    <tr>
                        {WEEKDAYS.map((d) => (
                            <th
                                key={d}
                                className="pb-2 text-xs font-medium text-gray-500"
                            >
                                {d}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {matrix.map((week, i) => (
                        <tr key={i}>
                            {week.map(({ date, currentMonth }, j) => {
                                const selected = isSameDay(date, value)
                                const disabled =
                                    !currentMonth || !canSelect(date)
                                return (
                                    <td key={j} className="py-1">
                                        <button
                                            className={`w-8 h-8 rounded-full transition
                                                ${selected ? 'bg-[#A78BFA] text-white font-bold' : ''}
                                                ${!currentMonth ? 'text-[#B3B3B3]' : ''}
                                                ${!disabled && !selected && 'hover:bg-[#E9DFFC]'}
                                                ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
                                            `}
                                            disabled={disabled}
                                            onClick={() =>
                                                onChange(new Date(date))
                                            }
                                            tabIndex={disabled ? -1 : 0}
                                            type="button"
                                        >
                                            {renderDay
                                                ? renderDay(
                                                      date,
                                                      currentMonth,
                                                      selected
                                                  )
                                                : date.getDate()}
                                        </button>
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

export default Calendar

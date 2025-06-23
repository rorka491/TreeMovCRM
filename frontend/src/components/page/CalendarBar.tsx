import Select from '../Select'
import { useMatch, useNavigate } from 'react-router-dom'
import { getWeekRange } from '../../lib/getWeekRange'

const VIEW_OPTIONS = [
    { value: 'День', key: 'by-day' },
    { value: 'Неделя', key: 'by-week' },
    { value: 'Месяц', key: 'by-month' },
]

const RADIO_OPTIONS = [
    {
        value: 'list',
        width: 14,
        height: 12,
        icon: (
            <>
                <path
                    d="M1.5 1.5L12.5 1.5"
                    stroke="#B5B5B5"
                    strokeWidth="2"
                    strokeLinecap="round"
                />
                <path
                    d="M1.5 4.5L12.5 4.5"
                    stroke="#B5B5B5"
                    strokeWidth="2"
                    strokeLinecap="round"
                />
                <path
                    d="M1.5 7.5L12.5 7.5"
                    stroke="#B5B5B5"
                    strokeWidth="2"
                    strokeLinecap="round"
                />
                <path
                    d="M1.5 10.5L12.5 10.5"
                    stroke="#B5B5B5"
                    strokeWidth="2"
                    strokeLinecap="round"
                />
            </>
        ),
    },
    {
        value: '',
        width: 18,
        height: 18,
        icon: (
            <>
                <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M4.5 3H13.5C14.2956 3 15.0587 3.31607 15.6213 3.87868C16.1839 4.44129 16.5 5.20435 16.5 6V13.5C16.5 14.2956 16.1839 15.0587 15.6213 15.6213C15.0587 16.1839 14.2956 16.5 13.5 16.5H4.5C3.70435 16.5 2.94129 16.1839 2.37868 15.6213C1.81607 15.0587 1.5 14.2956 1.5 13.5V6C1.5 5.20435 1.81607 4.44129 2.37868 3.87868C2.94129 3.31607 3.70435 3 4.5 3ZM4.5 4.5C4.10218 4.5 3.72064 4.65804 3.43934 4.93934C3.15804 5.22064 3 5.60218 3 6V13.5C3 13.8978 3.15804 14.2794 3.43934 14.5607C3.72064 14.842 4.10218 15 4.5 15H13.5C13.8978 15 14.2794 14.842 14.5607 14.5607C14.842 14.2794 15 13.8978 15 13.5V6C15 5.60218 14.842 5.22064 14.5607 4.93934C14.2794 4.65804 13.8978 4.5 13.5 4.5H4.5Z"
                    fill="#808080"
                    fillOpacity="0.55"
                />
                <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M2.25 7.5C2.25 7.30109 2.32902 7.11032 2.46967 6.96967C2.61032 6.82902 2.80109 6.75 3 6.75H15C15.1989 6.75 15.3897 6.82902 15.5303 6.96967C15.671 7.11032 15.75 7.30109 15.75 7.5C15.75 7.69891 15.671 7.88968 15.5303 8.03033C15.3897 8.17098 15.1989 8.25 15 8.25H3C2.80109 8.25 2.61032 8.17098 2.46967 8.03033C2.32902 7.88968 2.25 7.69891 2.25 7.5ZM6 1.5C6.19891 1.5 6.38968 1.57902 6.53033 1.71967C6.67098 1.86032 6.75 2.05109 6.75 2.25V5.25C6.75 5.44891 6.67098 5.63968 6.53033 5.78033C6.38968 5.92098 6.19891 6 6 6C5.80109 6 5.61032 5.92098 5.46967 5.78033C5.32902 5.63968 5.25 5.44891 5.25 5.25V2.25C5.25 2.05109 5.32902 1.86032 5.46967 1.71967C5.61032 1.57902 5.80109 1.5 6 1.5ZM12 1.5C12.1989 1.5 12.3897 1.57902 12.5303 1.71967C12.671 1.86032 12.75 2.05109 12.75 2.25V5.25C12.75 5.44891 12.671 5.63968 12.5303 5.78033C12.3897 5.92098 12.19891 6 12 6C11.8011 6 11.6103 5.92098 11.4697 5.78033C11.329 5.63968 11.25 5.44891 11.25 5.25V2.25C11.25 2.05109 11.329 1.86032 11.4697 1.71967C11.6103 1.57902 11.8011 1.5 12 1.5Z"
                    fill="#808080"
                    fillOpacity="0.55"
                />
                <path
                    d="M6 9.75C6 9.94891 5.92098 10.1397 5.78033 10.2803C5.63968 10.421 5.44891 10.5 5.25 10.5C5.05109 10.5 4.86032 10.421 4.71967 10.2803C4.57902 10.1397 4.5 9.94891 4.5 9.75C4.5 9.55109 4.57902 9.36032 4.71967 9.21967C4.86032 9.07902 5.05109 9 5.25 9C5.44891 9 5.63968 9.07902 5.78033 9.21967C5.92098 9.36032 6 9.55109 6 9.75ZM6 12.75C6 12.9489 5.92098 13.1397 5.78033 13.2803C5.63968 13.421 5.44891 13.5 5.25 13.5C5.05109 13.5 4.86032 13.421 4.71967 13.2803C4.57902 13.1397 4.5 12.9489 4.5 12.75C4.5 12.5511 4.57902 12.3603 4.71967 12.2197C4.86032 12.079 5.05109 12 5.25 12C5.44891 12 5.63968 12.079 5.78033 12.2197C5.92098 12.3603 6 12.5511 6 12.75ZM9.75 9.75C9.75 9.94891 9.67098 10.1397 9.53033 10.2803C9.38968 10.421 9.19891 10.5 9 10.5C8.80109 10.5 8.61032 10.421 8.46967 10.2803C8.32902 10.1397 8.25 9.94891 8.25 9.75C8.25 9.55109 8.32902 9.36032 8.46967 9.21967C8.61032 9.07902 8.80109 9 9 9C9.19891 9 9.38968 9.07902 9.53033 9.21967C9.67098 9.36032 9.75 9.55109 9.75 9.75ZM9.75 12.75C9.75 12.9489 9.67098 13.1397 9.53033 13.2803C9.38968 13.421 9.19891 13.5 9 13.5C8.80109 13.5 8.61032 13.421 8.46967 13.2803C8.32902 13.1397 8.25 12.9489 8.25 12.75C8.25 12.5511 8.32902 12.3603 8.46967 12.2197C8.61032 12.079 8.80109 12 9 12C9.19891 12 9.38968 12.079 9.53033 12.2197C9.67098 12.3603 9.75 12.5511 9.75 12.75ZM13.5 9.75C13.5 9.94891 13.421 10.1397 13.2803 10.2803C13.1397 10.421 12.9489 10.5 12.75 10.5C12.5511 10.5 12.3603 10.421 12.2197 10.2803C12.079 10.1397 12 9.94891 12 9.75C12 9.55109 12.079 9.36032 12.2197 9.21967C12.3603 9.07902 12.5511 9 12.75 9C12.9489 9 13.1397 9.07902 13.2803 9.21967C13.421 9.36032 13.5 9.55109 13.5 9.75ZM13.5 12.75C13.5 12.9489 13.421 13.1397 13.2803 13.2803C13.1397 13.421 12.9489 13.5 12.75 13.5C12.5511 13.5 12.3603 13.421 12.2197 13.2803C12.079 13.1397 12 12.9489 12 12.75C12 12.5511 12.079 12.3603 12.2197 12.2197C12.3603 12.079 12.5511 12 12.75 12C12.9489 12 13.1397 12.079 13.2803 12.2197C13.421 12.3603 13.5 12.5511 13.5 12.75Z"
                    fill="#808080"
                    fillOpacity="0.55"
                />
            </>
        ),
    },
]

function CalendarBar({
    currentDate,
    setCurrentDate,
}: {
    currentDate: Date
    setCurrentDate: React.Dispatch<React.SetStateAction<Date>>
}) {
    const match = useMatch('/:any/:lastPart/*')
    const activeSection: string = match?.params?.lastPart || 'by-month'
    const activeParamsEnd = match?.params?.['*'] || ''
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

    const changeDate = (amount: number, type: string) => {
        const newDate = new Date(currentDate)
        if (type === 'by-day') newDate.setDate(date + amount)
        else if (type === 'by-week') newDate.setDate(date + amount * 7)
        else newDate.setMonth(month + amount, 1)
        setCurrentDate(newDate)
    }

    return (
        <div className="flex items-center justify-between">
            <div className="flex gap-[6px] items-center *:cursor-pointer">
                <button
                    onClick={() => changeDate(-1, activeSection)}
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
                    onClick={() => changeDate(1, activeSection)}
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
                    onSelected={(newSelected) =>
                        navigate(
                            '/schedule/' +
                                newSelected.key +
                                '/' +
                                activeParamsEnd
                        )
                    }
                />
                <div className="flex gap-2">
                    {RADIO_OPTIONS.map((opt) => (
                        <label key={opt.value}>
                            <input
                                type="radio"
                                name="calendar-view"
                                className="hidden peer"
                                value={opt.value}
                                checked={
                                    activeParamsEnd.slice(0, 4) === opt.value
                                }
                                onChange={() =>
                                    navigate(
                                        '/schedule/' +
                                            activeSection +
                                            '/' +
                                            opt.value
                                    )
                                }
                            />
                            <span className="w-[36px] h-[26px] rounded-full border border-[#E0E0E0] flex items-center justify-center peer-checked:bg-[#EDE8FE] cursor-pointer">
                                <svg
                                    width={opt.width}
                                    height={opt.height}
                                    fill="none"
                                    viewBox={`0 0 ${opt.width} ${opt.height}`}
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

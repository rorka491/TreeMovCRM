import { useState } from 'react'
import Select from '../Select'
import { useNavigate } from 'react-router-dom'

function CalendarBar({
    currentDate,
    setCurrentDate,
}: {
    currentDate: Date
    setCurrentDate: (d: Date) => void
}) {
    const [selected, setSelected] = useState<{ value: string; key: string }>({
        value: 'Месяц',
        key: 'month',
    })

    const year = currentDate.getFullYear()
    const month = currentDate.getMonth()

    const monthYear = currentDate.toLocaleString('ru-RU', {
        month: 'long',
        year: 'numeric',
    })

    const navigate = useNavigate()

    return (
        <div className="flex items-center justify-between ">
            <div className="flex gap-[6px] items-center *:cursor-pointer">
                <button
                    onClick={() => setCurrentDate(new Date(year, month - 1, 1))}
                    className="grid place-items-center w-[20px] h-[20px] border-[#616161] border rounded-full"
                    aria-label="Предыдущий месяц"
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
                    onClick={() => setCurrentDate(new Date(year, month + 1, 1))}
                    className="grid place-items-center w-[20px] h-[20px] border-[#616161] border rounded-full"
                    aria-label="Следующий месяц"
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
                    onClick={() => setCurrentDate(new Date())}
                    className="font-semibold"
                >
                    {monthYear[0].toUpperCase() + monthYear.slice(1)}
                </button>
            </div>
            <div>
                <div className="flex items-center gap-2">
                    <Select
                        options={[
                            { value: 'День', key: 'day' },
                            { value: 'Неделя', key: 'week' },
                            { value: 'Месяц', key: 'month' },
                        ]}
                        className="h-[26px]"
                        placeholder={selected.value}
                        onSelected={(newSelected: {
                            value: string
                            key: string
                        }) => {
                            setSelected(newSelected)
                            navigate('/shedules/' + newSelected.key)
                        }}
                    />
                    <div className="flex gap-2">
                        <label>
                            <input
                                type="radio"
                                name="calendar-view"
                                className="hidden peer"
                                value="list"
                                // checked={selectedView === 'list'}
                                // onChange={() => setSelectedView('list')}
                            />
                            <span className="w-[36px] h-[26px] rounded-full border border-[#E0E0E0] flex items-center justify-center peer-checked:bg-[#F4F2FF] cursor-pointer">
                                <svg
                                    width="20"
                                    height="20"
                                    fill="none"
                                    viewBox="0 0 20 20"
                                >
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
                                </svg>
                            </span>
                        </label>
                        <label>
                            <input
                                type="radio"
                                name="calendar-view"
                                className="hidden peer"
                                value="calendar"
                                // checked={selectedView === 'calendar'}
                                // onChange={() => setSelectedView('calendar')}
                            />
                            <span className="w-[36px] h-[26px] rounded-full border border-[#E0E0E0] flex items-center justify-center peer-checked:bg-[#F4F2FF] cursor-pointer">
                                <svg
                                    width="20"
                                    height="20"
                                    fill="none"
                                    viewBox="0 0 20 20"
                                >
                                    <rect
                                        x="3"
                                        y="5"
                                        width="14"
                                        height="12"
                                        rx="2"
                                        fill="#E1D8FB"
                                        stroke="#BDBDBD"
                                    />
                                    <rect
                                        x="6"
                                        y="9"
                                        width="2"
                                        height="2"
                                        rx="1"
                                        fill="#BDBDBD"
                                    />
                                    <rect
                                        x="10"
                                        y="9"
                                        width="2"
                                        height="2"
                                        rx="1"
                                        fill="#BDBDBD"
                                    />
                                    <rect
                                        x="14"
                                        y="9"
                                        width="2"
                                        height="2"
                                        rx="1"
                                        fill="#BDBDBD"
                                    />
                                    <rect
                                        x="6"
                                        y="13"
                                        width="2"
                                        height="2"
                                        rx="1"
                                        fill="#BDBDBD"
                                    />
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
                                    <rect
                                        x="7"
                                        y="3"
                                        width="1"
                                        height="3"
                                        rx=".5"
                                        fill="#BDBDBD"
                                    />
                                    <rect
                                        x="12"
                                        y="3"
                                        width="1"
                                        height="3"
                                        rx=".5"
                                        fill="#BDBDBD"
                                    />
                                </svg>
                            </span>
                        </label>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default CalendarBar

import { Outlet, useMatch, useNavigate } from 'react-router-dom'
import { FilterBar } from '../../components/page/FilterBar'
import { useState } from 'react'
import CalendarBar from '../../components/page/CalendarBar'
import { Lesson } from '../../components/LessonCard'
import { weekDays } from '../../lib/calendarConstants'
import CategoryBar from '../../components/page/CategoryBar'

const data: Lesson[] = [
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
        title: 'Биология',
        start_time: '15:00:00',
        end_time: '16:30:00',
        date: '21.06.2025',
        teacher: 8,
        week_day: 6,
        classroom: {
            title: '401',
            floor: 4,
            building: 1,
        },
        group: 104,
        subject: {
            name: 'Ботаника',
            teacher: 'Васильев В.В.',
            color: '#27ae60',
        },
        is_canceled: false,
        is_completed: false,
        lesson: 8,
    },
    {
        title: 'География',
        start_time: '11:00:00',
        end_time: '12:30:00',
        date: '22.06.2025',
        teacher: 9,
        week_day: 7,
        classroom: {
            title: '502',
            floor: 5,
            building: 1,
        },
        group: 105,
        subject: {
            name: 'Физическая география',
            teacher: 'Громов Г.Г.',
            color: '#2980b9',
        },
        is_canceled: false,
        is_completed: false,
        lesson: 9,
    },
    {
        title: 'Английский язык',
        start_time: '08:30:00',
        end_time: '10:00:00',
        date: '23.06.2025',
        teacher: 10,
        week_day: 1,
        classroom: {
            title: '601',
            floor: 6,
            building: 2,
        },
        group: 106,
        subject: {
            name: 'Грамматика',
            teacher: 'Браун Дж.',
            color: '#8e44ad',
        },
        is_canceled: false,
        is_completed: false,
        lesson: 10,
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
        start_time: '10:05:00',
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

export function Schedule() {
    const [currentDate, setCurrentDate] = useState(new Date())
    const [lessons, setLessons] = useState<Lesson[]>(data)

    function upsertLesson(newLesson: Lesson) {
        setLessons((prevLessons) => {
            const idx = prevLessons.findIndex(
                (l) => l.lesson === newLesson.lesson
            )
            if (idx !== -1) {
                // обновляем существующий урок
                const updated = [...prevLessons]
                updated[idx] = newLesson
                return updated
            } else {
                // добавляем новый урок
                return [...prevLessons, newLesson]
            }
        })
    }

    const [filtersSelected, setFiltersSelected] = useState<{
        [k: string]: any | undefined
    }>({})
    const [filterData, setFilterData] = useState([
        {
            id: 'teacher',
            label: 'Преводователь',
            options: ['Роман', 'Никита', 'Родион'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'group',
            label: 'Группа',
            options: ['A', 'B'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'subject',
            label: 'Предмет',
            options: ['Информатика', 'История'],
            multiple: true,
            search: true,
            removeButton: true,
        },
        {
            id: 'data',
            label: 'Дата',
            date: true,
            options: ['11.11.1111', '11.22.3333'],
            search: true,
        },
        {
            id: 'auditorium',
            label: 'Аудитория',
            options: ['600', '1000'],
            multiple: true,
            search: true,
            removeButton: true,
        },
    ])

    const match = useMatch('/:any/:lastPart/*')
    const typeOfSchedule: string = match?.params?.lastPart || 'by-month'
    const activeParamsEnd: string = match?.params?.['*'] || ''

    const navigate = useNavigate()

    return (
        <section className="flex flex-col h-full gap-y-4">
            <CategoryBar categories={[]} searchPlaceholder='Найти в расписании...'></CategoryBar>
            <FilterBar
                disableAddButton={true}
                filterData={filterData}
                selectedChange={setFiltersSelected}
            />
            <CalendarBar
                currentDate={currentDate}
                setCurrentDate={setCurrentDate}
            />
            {activeParamsEnd === 'list' ? (
                <div className="relative w-full overflow-y-auto h-[60vh]">
                    <Outlet
                        context={{
                            currentDate,
                            lessons,
                            setCurrentDate,
                            upsertLesson,
                        }}
                    />
                </div>
            ) : (
                <div className="relative w-full overflow-y-auto h-[60vh]  special-scroll">
                    <table className="w-full bg-[#EAECF0] border rounded-xl overflow-hidden">
                        <thead className="sticky top-0">
                            <tr>
                                {typeOfSchedule !== 'by-month' && (
                                    <th className="w-24 font-normal bg-white">
                                        Часы
                                    </th>
                                )}
                                {typeOfSchedule === 'by-day' && (
                                    <th className="p-2 font-semibold text-left bg-[#EDE8FE]">
                                        {weekDays[currentDate.getDay()]}
                                    </th>
                                )}
                                {typeOfSchedule !== 'by-day' &&
                                    weekDays.map((d, i) => {
                                        const startOfWeek = new Date(
                                            currentDate
                                        )
                                        startOfWeek.setDate(
                                            currentDate.getDate() -
                                                startOfWeek.getDay()
                                        )
                                        const dayOfWeek = new Date(startOfWeek)
                                        dayOfWeek.setDate(
                                            startOfWeek.getDate() + i + 1
                                        )
                                        const dayNum = dayOfWeek.getDate()
                                        return (
                                            <th
                                                onClick={() => {
                                                    navigate('/schedule/by-day')
                                                    currentDate.setDate(
                                                        currentDate.getDate() +
                                                            i
                                                    )
                                                }}
                                                key={i}
                                                className="p-2 font-semibold text-center transition bg-[#EDE8FE]"
                                            >
                                                {d}{' '}
                                                {typeOfSchedule === 'by-week'
                                                    ? dayNum
                                                    : ''}
                                            </th>
                                        )
                                    })}
                            </tr>
                        </thead>
                        <Outlet
                            context={{
                                currentDate,
                                lessons,
                                setCurrentDate,
                                upsertLesson,
                            }}
                        />
                    </table>
                </div>
            )}
        </section>
    )
}

export default Schedule

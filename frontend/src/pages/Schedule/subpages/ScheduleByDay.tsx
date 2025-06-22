import { useOutletContext } from 'react-router-dom'
import LessonCard, { Lesson } from '../../../components/LessonCard/LessonCard'
import { formatDate } from '../../../lib/formatDate'
import { isLessonInHour } from '../../../lib/isLessonInHour'

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

const hours = Array.from({ length: 24 }, (_, i) => i + ':00')

const WEEKDAYS = ['Вс', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Пн']

function ScheduleByDay() {
    const currentDate: Date = useOutletContext()
    return (
        <section className="flex flex-col w-full h-full gap-4 bg-[#F7F7FA] min-h-screen">
            <div className="w-full overflow-y-scroll h-[60vh] special-scroll">
                <table className="w-full bg-[#EAECF0] border rounded-[12.5px] overflow-hidden">
                    <thead>
                        <tr>
                            <th className="text-base font-normal w-[100px] border-[#EAECF0] bg-white">
                                Часы
                            </th>
                            <th className="font-semibold border align-top text-left p-[8px] border-[#EAECF0] bg-[#A78BFA33] select-none">
                                {WEEKDAYS[currentDate.getDay()] +
                                    ' ' +
                                    currentDate.getDate()}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {hours.map((hour, rowIdx) => {
                            const lessonsInHour = lessons.filter((l) =>
                                isLessonInHour(l, hour, formatDate(currentDate))
                            )
                            return (
                                <tr key={rowIdx}>
                                    <td className="text-center h-[125px] bg-white relative border align-top transition p-[8px] hover:bg-gray-100 border-[#EAECF0] cursor-pointer select-none">
                                        {hour}
                                    </td>
                                    <td className="h-[125px] bg-white relative border align-top transition p-[8px] hover:bg-gray-100 border-[#EAECF0] cursor-pointer select-none">
                                        <div className="flex h-full gap-2">
                                            {lessonsInHour.map((lesson) => (
                                                <LessonCard
                                                    key={lesson.title}
                                                    lesson={lesson}
                                                />
                                            ))}
                                        </div>
                                    </td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        </section>
    )
}

export default ScheduleByDay

import { useMatch, useOutletContext } from 'react-router-dom'
import { Table } from '../../../components/Table'
import { formatDate } from '../../../lib/formatDate'
import { Lesson } from '../../../components/LessonCard'
import { useEffect, useState } from 'react'
import { filterLessons } from '../../../lib/filterLessons'

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

function SheduleList() {
    const {
        currentDate,
        lessons,
    }: {
        currentDate: Date
        lessons: Lesson[]
        upsertLesson: (newLesson: Lesson) => void
    } = useOutletContext()

    const [data, setData] = useState<Lesson[]>([])

    const match = useMatch('/:any/:lastPart/*')
    const typeOfSchedule: string = match?.params?.lastPart || 'by-month'

    useEffect(() => {
        setData(filterLessons(lessons, currentDate, typeOfSchedule))
    }, [lessons, currentDate])

    return (
        <div className="w-full h-full bg-[#F7F7FA] p-4">
            <Table<Lesson>
                keys={{
                    start_time: 'Время',
                    subject: 'Предмет',
                    classroom: 'Кабинет',
                    teacher: 'Преподаватель',
                    group: 'Группа',
                }}
                data={data}
                mapFields={{
                    start_time: (row) =>
                        `${row.start_time.slice(0, 5)} - ${row.end_time.slice(0, 5)}`,
                    subject: (row) => row.subject.name,
                    classroom: (row) => row.classroom.title,
                    teacher: (row) => row.subject.teacher,
                    group: (row) => row.group,
                }}
                showSkeleton={false}
            />
        </div>
    )
}

export default SheduleList

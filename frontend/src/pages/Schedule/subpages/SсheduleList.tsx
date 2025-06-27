import { useMatch, useOutletContext } from 'react-router-dom'
import { Table } from '../../../components/Table'
import { useEffect, useState } from 'react'
import { filterLessons } from '../../../lib/filterLessons'
import { Lesson } from '../../../api/api'

function SсheduleList() {
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
        let filtered = filterLessons(lessons, currentDate, typeOfSchedule)
        // Если выбран режим "by-month", фильтруем только текущий месяц
        if (typeOfSchedule === 'by-month') {
            filtered = filtered.filter((l) => {
                const [day, month, year] = l.date.split('.').map(Number)
                return (
                    month === currentDate.getMonth() + 1 &&
                    year === currentDate.getFullYear()
                )
            })
        }
        setData(filtered)
    }, [lessons, currentDate, typeOfSchedule])
    console.log(data)
    return data.length !== 0 ? (
        <Table
            keys={{
                date: 'Дата',
                start_time: 'Время',
                subject: 'Предмет',
                classroom: 'Кабинет',
                teacher: 'Преподаватель',
                group: 'Группа',
            }}
            data={data}
            mapFields={{
                date: (row) => row.date,
                start_time: (row) =>
                    `${row.start_time.slice(0, 5)} - ${row.end_time.slice(0, 5)}`,
                subject: (row) => row.subject.name,
                classroom: (row) => row.classroom.title,
                teacher: (row) => row.subject.teacher,
                group: (row) => row.group,
            }}
            showSkeleton={!lessons}
            skeletonAmount={20}
        />
    ) : (
        <div className="flex flex-col items-center justify-center w-full h-full">
            <h3 className="text-4xl">Пусто =(</h3>
            <p>Данных за текущий период не найдено</p>
        </div>
    )
}

export default SсheduleList

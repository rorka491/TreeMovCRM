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
    } = useOutletContext()

    const [data, setData] = useState<Lesson[]>([])

    const match = useMatch('/:any/:lastPart/*')
    const typeOfSchedule: string = match?.params?.lastPart || 'by-month'

    useEffect(() => {
        let filtered = filterLessons(lessons, currentDate, typeOfSchedule)
        // Если выбран режим "by-month", фильтруем только текущий месяц
        if (typeOfSchedule === 'by-month') {
            filtered = filtered.filter((l) => {
                const [_, month, year] = l.date.split('.').map(Number)
                return (
                    month === currentDate.getMonth() + 1 &&
                    year === currentDate.getFullYear()
                )
            })
        }
        setData(filtered)
    }, [lessons, currentDate, typeOfSchedule])

    return (
        <div className="relative w-full overflow-y-auto h-[60vh]">
            {data.length !== 0 ? (
                <Table
                    keys={{
                        date: 'Дата',
                        start_time: {
                            type: 'map',
                            str: 'Время',
                            f: (row) =>
                                `${row.start_time.slice(0, 5)} - ${row.end_time.slice(0, 5)}`,
                        },
                        subject: { type: 'flat', keys: { name: 'Предмет' } },
                        classroom: { type: 'flat', keys: { title: 'Кабинет' } },
                        teacher: {
                            type: 'flat',
                            keys: {
                                employer: {
                                    type: 'join',
                                    str: 'Преподаватель',
                                    keys: ['surname', 'name', 'patronymic'],
                                },
                            },
                        },
                        group: {
                            type: 'flat',
                            keys: { name: 'Группа' },
                        },
                    }}
                    data={data}
                    showSkeleton={!lessons}
                    skeletonAmount={20}
                />
            ) : (
                <div className="flex flex-col items-center justify-center w-full h-full">
                    <h3 className="text-4xl">Пусто =(</h3>
                    <p>Данных за текущий период не найдено</p>
                </div>
            )}
        </div>
    )
}

export default SсheduleList

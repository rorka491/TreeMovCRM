import { Outlet } from 'react-router-dom'
import { filter, FilterBar, FilterPart } from '../../components/page/FilterBar'
import { useEffect, useState } from 'react'
import CalendarBar from '../../components/page/CalendarBar'
import CategoryBar from '../../components/page/CategoryBar'
import { api } from '../../api'
import { useLessons } from './hooks/useLessons'

export function Schedule() {
    const [currentDate, setCurrentDate] = useState(new Date())
    const [lessons] = useLessons(
        currentDate,
        new Date(+currentDate + 31 * 24 * 60 * 60 * 1000)
    )

    const [filtersSelected, setFiltersSelected] = useState<{
        [k: string]: any
    }>({})
    const [filterData, setFilterData] = useState<FilterPart[]>([
        {
            id: 'teacher',
            label: 'Преводователь',
            options: ['Роман', 'Никита', 'Родион'],
            search: true,
            removeButton: true,
            multiple: true,
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
            id: 'auditorium',
            label: 'Аудитория',
            options: ['600', '1000'],
            multiple: true,
            search: true,
            removeButton: true,
        },
    ])

    useEffect(() => {
        api.schedules.getTeachers().then((teachers) => {
            // @ts-ignore
            filterData[0].options = teachers.map(
                (teacher) => teacher.employer.name
            )

            setFilterData([...filterData])
        })

        api.students.getAllGroups().then((groups) => {
            // @ts-ignore
            filterData[1].options = groups
            setFilterData([...filterData])
        })

        api.schedules.getSubjects().then((subjects) => {
            // @ts-ignore
            filterData[2].options = subjects.map((sub) => sub.name)
            setFilterData([...filterData])
        })
    }, [])

    return (
        <section className="flex flex-col h-full gap-y-4">
            <CategoryBar
                categories={[]}
                searchPlaceholder="Найти в расписании..."
                searchOptions={lessons.map((lesson) => ({
                    id: lesson.id,
                    onSelect: () => {},
                    object: lesson,
                    title: `${lesson.subject.name} ${lesson.classroom.title} ${lesson.date} ${lesson.start_time.split(':').slice(0, 2).join(':')}`,
                }))}
            />
            <FilterBar
                disableAddButton={true}
                filterData={filterData}
                selectedChange={setFiltersSelected}
            />
            <CalendarBar
                currentDate={currentDate}
                setCurrentDate={setCurrentDate}
            />
            <Outlet
                context={{
                    currentDate,
                    lessons: filter(
                        lessons,
                        {
                            teacher: {
                                type: 'includes',
                                filterId: 'teacher',
                                mapValue: (teacher) => teacher.employer.name,
                            },
                            group: {
                                type: 'includes',
                                mapValue: (group) => group.name,
                            },
                            subject: {
                                type: 'includes',
                                mapValue: (subject) => subject.name,
                            },
                        },
                        filtersSelected
                    ),
                    setCurrentDate,
                }}
            />
        </section>
    )
}

export default Schedule

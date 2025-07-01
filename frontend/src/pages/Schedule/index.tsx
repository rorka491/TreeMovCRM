import { Outlet } from 'react-router-dom'
import { filter, FilterBar, FilterPart } from '../../components/page/FilterBar'
import { useEffect, useState } from 'react'
import CalendarBar from '../../components/page/CalendarBar'
import CategoryBar from '../../components/page/CategoryBar'
import { api } from '../../api'
import { useLessons } from './hooks/useLessons'
import { Lesson } from '../../api/api'
import { debounce } from '../../lib/debounce'
import { parseDate } from '../../lib/parseDate'

export function Schedule() {
    const [currentDate, setCurrentDate] = useState(new Date())
    const [lessons] = useLessons(
        currentDate,
        new Date(+currentDate + 31 * 24 * 60 * 60 * 1000)
    )

    const [searchLessons, setSearchLessons] = useState<Lesson[]>(lessons)

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

    const onSearchChange = debounce((s: string) => {
        if (s === "") {
            return
        }
        
        api.schedules.getSearch(s).then(setSearchLessons)
    }, 400)

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

        api.schedules.getClassrooms().then((classrooms) => {
            // @ts-ignore
            filterData[3].options = classrooms.map((sub) => sub.title)
            setFilterData([...filterData])
        })
    }, [])

    return (
        <section className="flex flex-col h-full gap-y-4">
            <CategoryBar
                categories={[]}
                searchPlaceholder="Найти в расписании..."
                searchOptions={searchLessons.map((lesson) => ({
                    id: lesson.id,
                    onSelect: (lesson: Lesson) => {
                        console.log(lesson)
                        console.log(lesson.date, parseDate(lesson.date))
                        setCurrentDate(parseDate(lesson.date))
                    },
                    object: lesson,
                    title: `${lesson.subject.name} ${lesson.classroom.title} ${lesson.date} ${lesson.start_time.split(':').slice(0, 2).join(':')}`,
                }))}
                onSearchInputChange={onSearchChange}
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
                            classroom: {
                                type: 'includes',
                                mapValue: (c) => c.title,
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

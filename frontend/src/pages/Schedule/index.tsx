import { Outlet, useMatch, useNavigate } from 'react-router-dom'
import { FilterBar, FilterPart } from '../../components/page/FilterBar'
import { useEffect, useState } from 'react'
import CalendarBar from '../../components/page/CalendarBar'
import { weekDaysShort } from '../../lib/calendarConstants'
import CategoryBar from '../../components/page/CategoryBar'
import { api } from '../../api'
import { Lesson } from '../../api/api'

export function Schedule() {
    const [currentDate, setCurrentDate] = useState(new Date())
    let [lessons, setLessons] = useState<Lesson[]>([])

    useEffect(() => {
        api.schedules.getAll().then((lessons) => setLessons(lessons))
    }, [])

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
            type: 'date',
            id: 'data',
            label: 'Дата',
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
        })

        api.schedules.getSubjects().then((subjects) => {})
    }, [])

    lessons = lessons
        .filter(
            (lesson) =>
                !filtersSelected.teacher ||
                filtersSelected.teacher.length === 0 ||
                filtersSelected.teacher.some(
                    (t) => t === lesson?.teacher?.employer?.name
                )
        )
        .filter(
            (lesson) =>
                !filtersSelected.group ||
                filtersSelected.group.length === 0 ||
                filtersSelected.group.some((g) => g === lesson.group.name)
        )

    return (
        <section className="flex flex-col h-full gap-y-4">
            <CategoryBar
                categories={[
                    {
                        url: 'main',
                        label: 'Основное',
                    },
                    {
                        url: 'guideline',
                        label: 'Справочник',
                    },
                ]}
                searchPlaceholder="Найти в расписании..."
            ></CategoryBar>
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
                    lessons,
                    setCurrentDate,
                    upsertLesson,
                }}
            />
        </section>
    )
}

export default Schedule

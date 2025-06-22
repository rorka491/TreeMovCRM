import { useOutletContext } from 'react-router-dom'
import LessonCard, { Lesson } from '../../../components/LessonCard/LessonCard'

const lessons: Lesson[] = [
    {
        id: 1,
        title: 'Астрономия',
        teacher: 'Антон Журавлев, Артемий Грек',
        classroom: '32',
        color: '#7DECF6',
        start: '10:00',
        end: '12:10',
        groups: '1, 7, 4 группы',
    },
    {
        id: 2,
        title: 'История',
        teacher: 'Иосиф Хрунов',
        classroom: '201',
        color: '#FFE066',
        start: '12:30',
        end: '14:00',
        groups: '5, 6, 1 группы',
    },
    {
        id: 3,
        title: 'Танцы',
        teacher: 'Борис Синяков',
        classroom: '436/7',
        color: '#6EC1E4',
        start: '12:30',
        end: '14:00',
        groups: '12 группа',
    },
    {
        id: 4,
        title: 'Математика',
        teacher: 'Иосиф Хрунов',
        classroom: '205',
        color: '#E6B3FF',
        start: '12:30',
        end: '13:30',
        groups: '5, 4, 1 группы',
    },
    {
        id: 5,
        title: 'Французский',
        teacher: 'Борис Синяков',
        classroom: '436/7',
        color: '#FF5B5B',
        start: '12:45',
        end: '14:00',
        groups: '12 группа',
    },
    {
        id: 6,
        title: 'Русский',
        teacher: 'Борис Синяков',
        classroom: '436/7',
        color: '#FFD966',
        start: '12:45',
        end: '14:00',
        groups: '12 группа',
    },
]

const hours = Array.from({ length: 24 }, (_, i) => i + ':00')

const WEEKDAYS = ['Вс', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Пн']

function isLessonInHour(lesson: Lesson, hour: string) {
    const [hStart, mStart] = lesson.start.split(':').map(Number)
    const [hEnd, mEnd] = lesson.end.split(':').map(Number)
    const [h, m] = hour.split(':').map(Number)
    const lessonStart = hStart * 60 + mStart
    const lessonEnd = hEnd * 60 + mEnd
    const time = h * 60 + m
    return time >= lessonStart && time < lessonEnd
}

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
                                isLessonInHour(l, hour)
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
                                                    key={lesson.id}
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

import React, { useState } from 'react'

type Lesson = {
    id: number
    title: string
    teacher: string
    classroom: string
    color: string
    start: string // '10:00'
    end: string // '12:10'
    groups?: string
    isCanceled?: boolean
    isCompleted?: boolean
}

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

const hours = [
    '9:00',
    '10:00',
    '11:00',
    '12:00',
    '13:00',
    '14:00',
    '15:00',
    '16:00',
]

function getLessonsForHour(hour: string) {
    // Возвращает уроки, которые начинаются в этот час
    return lessons.filter((l) => l.start.startsWith(hour.split(':')[0]))
}

function ScheduleByDay() {
    const [selectedLesson, setSelectedLesson] = useState<number | null>(null)

    return (
        <div className="w-full h-full bg-[#F7F7FB] rounded-[16px] p-4 flex flex-col">
            <div className="flex items-center pb-2 mb-2 border-b">
                <div className="mr-4 text-lg font-semibold">Часы</div>
                <div className="text-lg font-semibold">Пн 10</div>
            </div>
            <div className="flex-1 overflow-y-auto special-scroll">
                <div className="grid grid-cols-[80px_1fr] gap-x-2">
                    <div className="flex flex-col gap-y-8">
                        {hours.map((h) => (
                            <div
                                key={h}
                                className="h-[60px] flex items-start justify-end pr-2 text-gray-500 text-sm"
                            >
                                {h}
                            </div>
                        ))}
                    </div>
                    <div className="flex flex-col gap-y-2">
                        {hours.map((h, idx) => (
                            <div key={h} className="relative h-[60px]">
                                {/* Уроки, начинающиеся в этот час */}
                                {lessons
                                    .filter((l) =>
                                        l.start.startsWith(h.split(':')[0])
                                    )
                                    .map((l) => (
                                        <div
                                            key={l.id}
                                            className="absolute top-0 left-0 flex flex-col w-full gap-1 p-3 bg-white border shadow-sm cursor-pointer rounded-xl"
                                            style={{
                                                borderColor: l.color,
                                                borderWidth: 2,
                                            }}
                                            onClick={() =>
                                                setSelectedLesson(l.id)
                                            }
                                        >
                                            <div className="flex items-center gap-2">
                                                <span
                                                    className="w-3 h-3 rounded-full"
                                                    style={{
                                                        background: l.color,
                                                    }}
                                                ></span>
                                                <span className="font-medium">
                                                    {l.title}
                                                </span>
                                            </div>
                                            <div className="text-xs text-gray-500">
                                                {l.teacher}
                                            </div>
                                            <div className="text-xs text-gray-500">
                                                Каб. {l.classroom}
                                            </div>
                                            <div className="text-xs text-gray-500">
                                                {l.groups}
                                            </div>
                                            <div className="text-xs text-gray-400">
                                                {l.start}–{l.end}
                                            </div>
                                        </div>
                                    ))}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ScheduleByDay

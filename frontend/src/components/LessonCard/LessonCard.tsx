import { useState } from 'react'

export type Lesson = {
    id: number
    title: string
    teacher: string
    classroom: string
    color: string
    start: string
    end: string
    groups?: string
}

type LessonCardProps = {
    lesson: Lesson
}

function LessonCard({ lesson }: LessonCardProps) {
    const [expanded, setExpanded] = useState(false)

    return (
        <div
            className={`min-w-[180px] ${expanded ? 'w-max' : 'w-[180px]'} relative px-3 py-2 bg-white border rounded-xl flex flex-col justify-between items-start transition-all duration-200 cursor-pointer ellipsis overflow-hidden
                *:text-xs *:w-full *:overflow-hidden *:text-ellipsis *:whitespace-nowrap *:text-[#707070]
                `}
            style={{
                borderColor: lesson.color,
            }}
            onMouseEnter={() => setExpanded(true)}
            onMouseLeave={() => setExpanded(false)}
        >
            <div className="flex items-center w-full gap-2 mb-1">
                <span
                    className="inline-block h-[15px] rounded-[5px] aspect-square"
                    style={{
                        background: lesson.color,
                    }}
                ></span>
                <h4 className="text-base text-black">{lesson.title}</h4>
            </div>
            <span>{lesson.teacher}</span>
            <span>Каб. {lesson.classroom}</span>
            <span>{lesson.groups}</span>
            <span>
                {lesson.start}–{lesson.end}
            </span>
        </div>
    )
}

export default LessonCard

import { useState } from 'react'
export type Lesson = {
    title: string
    start_time: string
    end_time: string
    date: string
    teacher: number
    week_day: number
    classroom: {
        title: string
        floor: number
        building: number
    }
    group: number
    subject: {
        name: string
        teacher: string
        color: string
    }
    is_canceled: boolean
    is_completed: boolean
    lesson: number
}

type LessonCardProps = {
    lesson: Lesson
}

function LessonCard({ lesson }: LessonCardProps) {
    const [expanded, setExpanded] = useState(false)

    return (
        <div
            className={`h-full min-w-[180px] w-fit relative px-3 py-2 bg-white border rounded-xl flex flex-col  items-start transition-all duration-200 cursor-pointer
                *:text-xs *:w-full *:overflow-hidden *:text-ellipsis *:whitespace-nowrap *:text-[#707070]
                `}
            style={{
                borderColor: lesson.subject.color,
            }}
            // onMouseEnter={() => setExpanded(true)}
            // onMouseLeave={() => setExpanded(false)}
        >
            <div className="flex items-center w-full gap-2 mb-1">
                <span
                    className="inline-block h-[15px] rounded-[5px] aspect-square"
                    style={{
                        background: lesson.subject.color,
                    }}
                ></span>
                <h4 className="overflow-hidden text-base text-black text-ellipsis">
                    {lesson.title}
                </h4>
            </div>
            <span>{lesson.subject.teacher}</span>
            <span>Каб. {lesson.classroom.title}</span>
            <span>{lesson.group}</span>
            <span>
                {lesson.start_time.slice(0, -3)} -{' '}
                {lesson.end_time.slice(0, -3)}
            </span>
        </div>
    )
}

export default LessonCard

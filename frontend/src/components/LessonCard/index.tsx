import { useState } from 'react'
import EditLessonPopUp from '../EditLessonPopUp'
import { PopUpMenu } from '../PopUpMenu'

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

function LessonCard({
    lesson,
    className = '',
    onClose,
    isPopUp = false,
    onSave,
}: {
    lesson: Lesson
    className?: string
    onClose?: () => void
    isPopUp?: boolean
    onSave: (updatedLesson: Lesson) => void
}) {
    const [isOpen, setIsOpen] = useState<boolean>(false)

    return (
        <>
            <div
                onClick={() => setIsOpen(true)}
                className={`${className} h-full relative px-3 py-2 bg-white border rounded-xl flex flex-col  items-start transition-all duration-200
                *:text-xs *:w-full *:overflow-hidden *:text-ellipsis *:whitespace-nowrap *:text-[#707070] 
                `}
                style={{
                    borderColor: lesson.subject.color,
                }}
            >
                <div className="flex items-center w-full gap-2 mb-1">
                    <span
                        className="inline-block h-[15px] rounded-[5px] aspect-square"
                        style={{
                            background: lesson.subject.color,
                        }}
                    ></span>
                    <h4 className="w-8/12 overflow-hidden text-base text-black text-ellipsis">
                        {lesson.title}
                    </h4>
                    {isPopUp && (
                        <span
                            className="h-[14px] w-[14px] cursor-pointer"
                            onClick={onClose}
                        >
                            <svg
                                width="14"
                                height="14"
                                viewBox="0 0 14 14"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M11.0827 3.739L10.2602 2.9165L6.99935 6.17734L3.73852 2.9165L2.91602 3.739L6.17685 6.99984L2.91602 10.2607L3.73852 11.0832L6.99935 7.82234L10.2602 11.0832L11.0827 10.2607L7.82185 6.99984L11.0827 3.739Z"
                                    fill="black"
                                />
                            </svg>
                        </span>
                    )}
                </div>
                <span>{lesson.subject.teacher}</span>
                <span>Каб. {lesson.classroom.title}</span>
                <span>{lesson.group}</span>
                <span>
                    {lesson.start_time.slice(0, -3)} -{' '}
                    {lesson.end_time.slice(0, -3)}
                </span>
            </div>
            {isOpen && (
                <PopUpMenu
                    open={isOpen}
                    onClose={() => setIsOpen(false)}
                    setOpen={() => setIsOpen(!isOpen)}
                >
                    <EditLessonPopUp
                        lesson={lesson}
                        onSave={(updatedLesson) => {
                            onSave(updatedLesson)
                            setIsOpen(false)
                        }}
                        onClose={() => setIsOpen(false)}
                    />
                </PopUpMenu>
            )}
        </>
    )
}

export default LessonCard

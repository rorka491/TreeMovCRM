import React, { useEffect, useState } from 'react'
import { Lesson, Teacher } from '../../api/api'
import Select from '../Select'
import { api } from '../../api'

function EditLessonPopUp({
    lesson,
    onClose,
    onSave,
}: {
    lesson: Lesson
    onClose: () => void
    onSave: (updatedLesson: Lesson) => void
}) {
    const [form, setForm] = useState({
        title: lesson.title,
        start_date: lesson.date,
        end_date: lesson.date,
        start_time: lesson.start_time,
        end_time: lesson.end_time,
        teacher: lesson.teacher.employer.name,
        classroom: lesson.classroom.title,
        group: lesson.group.toString(),
        description: '',
        color: lesson.subject.color,
        periodicity: '',
    })

    const [teachers, setTeachers] = useState<Teacher[]>([])
    const [selectedTeacher, setSelectedTeacher] = useState<Teacher | null>(null)

    useEffect(() => {
        api.schedules.getTeachers().then(setTeachers)
    }, [])

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
    ) => {
        const { name, value } = e.target
        setForm((prev) => ({ ...prev, [name]: value }))
    }

    const handleSave = (e: React.FormEvent) => {
        e.preventDefault()
        onSave({
            ...lesson,
            title: form.title,
            date: form.start_date,
            start_time: form.start_time,
            end_time: form.end_time,
            subject: {
                ...lesson.subject,
                teacher: form.teacher,
                color: form.color,
            },
            classroom: {
                ...lesson.classroom,
                title: form.classroom,
            },
            group: Number(form.group),
        })
    }

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/20"
            onClick={(e) => e.stopPropagation()}
        >
            <form
                className="bg-white rounded-2xl p-6 w-[370px] relative flex flex-col gap-3"
                onSubmit={handleSave}
            >
                <div className="flex items-center gap-2 mb-2">
                    <span
                        className="inline-block w-6 h-6 border rounded-md"
                        style={{ background: form.color }}
                    ></span>
                    <input
                        className="flex-1 text-lg font-medium bg-transparent border-none outline-none"
                        name="title"
                        value={form.title}
                        onChange={handleChange}
                        placeholder="Название"
                    />
                    <button
                        type="button"
                        className="absolute right-4 top-4"
                        onClick={onClose}
                        tabIndex={-1}
                    >
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 14 14"
                            fill="none"
                        >
                            <path
                                d="M11.0827 3.739L10.2602 2.9165L6.99935 6.17734L3.73852 2.9165L2.91602 3.739L6.17685 6.99984L2.91602 10.2607L3.73852 11.0832L6.99935 7.82234L10.2602 11.0832L11.0827 10.2607L7.82185 6.99984L11.0827 3.739Z"
                                fill="black"
                            />
                        </svg>
                    </button>
                </div>
                <div className="flex gap-2">
                    <input
                        type="time"
                        name="start_time"
                        value={form.start_time}
                        onChange={handleChange}
                        className="flex-1 px-2 py-1 border rounded"
                    />
                    <span className="self-center">—</span>
                    <input
                        type="time"
                        name="end_time"
                        value={form.end_time}
                        onChange={handleChange}
                        className="flex-1 px-2 py-1 border rounded"
                    />
                </div>
                <select
                    name="periodicity"
                    value={form.periodicity}
                    onChange={handleChange}
                    className="px-2 py-1 border rounded"
                >
                    <option value="">Периодичность</option>
                    <option value="once">Один раз</option>
                    <option value="weekly">Еженедельно</option>
                </select>
                <Select
                    options={teachers.map((t) => ({
                        key: t,
                        value: `${t.employer.surname} ${t.employer.name} ${t.employer.patronymic}`,
                    }))}
                    selected={
                        selectedTeacher
                            ? {
                                  key: selectedTeacher,
                                  value: `${selectedTeacher.employer.surname} ${selectedTeacher.employer.name} ${selectedTeacher.employer.patronymic}`,
                              }
                            : undefined
                    }
                    onSelected={({ key }) => {
                        setSelectedTeacher(key)
                    }}
                    searchQuery="Поиск преподавателя"
                />
                <input
                    name="classroom"
                    value={form.classroom}
                    onChange={handleChange}
                    placeholder="Аудитория"
                    className="py-1 border-b outline-none"
                />
                <input
                    name="group"
                    value={form.group}
                    onChange={handleChange}
                    placeholder="Группы"
                    className="py-1 border-b outline-none"
                />
                <input
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                    placeholder="Описание"
                    className="py-1 border-b outline-none"
                />
                <button
                    type="submit"
                    className="mt-3 bg-[#F5F5F5] rounded py-2 font-medium"
                >
                    Сохранить
                </button>
            </form>
        </div>
    )
}

export default EditLessonPopUp

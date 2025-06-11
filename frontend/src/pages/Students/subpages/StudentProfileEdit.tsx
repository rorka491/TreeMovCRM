import { useParams } from 'react-router-dom'
import { Student } from '../../../api/fakeApi'
import { useEffect, useState } from 'react'
import { api } from '../../../api'
import Select from '../../../components/Select'
import { months } from '../../../lib/months'
import { getDifferenceMonthsAndYears } from '../../../lib/getDifferenceMonthsAndYears'
import { parseDate } from '../../../lib/parseDate'
import { formatDate } from '../../../lib/formatDate'

function Input({
    label,
    name,
    onChange,
    value,
    className,
}: {
    label: string
    name: string
    onChange?: (s: string) => void
    value?: string
    className?: string
}) {
    const [val, setVal] = useState('')

    return (
        <label className={className + ' flex flex-col w-full'}>
            <span className="px-1 text-[#616161] font-bold">{label}</span>
            <input
                className="border-1 border-[#D9D9D9] bg-white rounded-[12.5px] text-[16px] px-2 py-[6px]"
                name={name}
                autoComplete="false"
                onChange={(e) => {
                    setVal(e.target.value)
                    onChange?.(e.target.value)
                }}
                value={value ?? val}
            />
        </label>
    )
}

export function StudentProfileEdit() {
    const { studentId } = useParams()
    const [student, setStudent] = useState<Student | undefined>(undefined)
    const [allGroups, setAllGroups] = useState<string[]>([])
    const [loaded, setLoaded] = useState(false)

    useEffect(() => {
        api.students.getById(studentId).then((s) => {
            setStudent(s)
            setLoaded(true)
        })

        api.students.getAllGroups().then(setAllGroups)
    }, [])

    return (
        <div className="border-t-2 h-[100%] p-4 flex gap-4">
            <div>
                <div className="relative min-w-[124px] rounded-full overflow-hidden w-[124px] h-[124px]">
                    <div className="absolute content-placeholder inset-0"></div>
                    <img
                        className="absolute object-cover block h-[100%] aspect-auto"
                        src={student?.img}
                        alt={student?.fullName}
                    />
                </div>
            </div>
            <div className="w-full max-w-[700px]">
                <form
                    onSubmit={(e) => {
                        e.preventDefault()
                    }}
                    className="flex flex-col gap-2"
                >
                    <div className="flex gap-4">
                        <Input
                            label="ФИО"
                            name="fullName"
                            value={student?.fullName}
                            onChange={(val) => {
                                if (!student) {
                                    return
                                }

                                student.fullName = val

                                setStudent({ ...student })
                            }}
                        />
                        <Input
                            label="Номер телефона"
                            name="phone"
                            value={student?.phone}
                            onChange={(val) => {
                                if (!student) {
                                    return
                                }

                                student.phone = val

                                setStudent({ ...student })
                            }}
                        />
                    </div>
                    <div className="flex gap-2 items-center">
                        <label className="flex flex-col">
                            <span className="px-1 text-[#616161] font-bold">
                                Дата рождения
                            </span>
                            <input
                                type="date"
                                className="border-2 border-solid p-2 rounded-2xl bg-white"
                                value={formatDate(
                                    parseDate(
                                        student?.dateOfBirth ?? '01.01.2000'
                                    ),
                                    'YYYY-MM-DD'
                                )}
                                onChange={(e) => {
                                    if (!student) {
                                        return
                                    }

                                    student.dateOfBirth = formatDate(
                                        new Date(e.target.value),
                                        'DD.MM.YYYY',
                                        { padDay: false }
                                    )

                                    setStudent({ ...student })
                                }}
                            />
                        </label>
                        <span className="ml-3 text-[#2F213EA6]">
                            {
                                getDifferenceMonthsAndYears(
                                    new Date(),
                                    parseDate(
                                        student?.dateOfBirth || '0.0.2000'
                                    )
                                )[1]
                            }{' '}
                            Лет
                        </span>
                    </div>
                    <Input
                        label="Почта"
                        name="email"
                        value={student?.email}
                        onChange={(val) => {
                            if (!student) {
                                return
                            }

                            student.email = val

                            setStudent({ ...student })
                        }}
                    />
                    <div className="flex gap-4 flex-wrap">
                        {student?.groups.map((group, i, allSelectedGroups) => (
                            <label key={group} className="flex flex-col">
                                <span className="px-1 text-[#616161] font-bold">
                                    Группа {i + 1}
                                </span>
                                <Select
                                    className="bg-white w-[min-content]"
                                    top="Удалить"
                                    topButton
                                    onTopButtonClick={() => {
                                        if (!student) {
                                            return
                                        }

                                        student.groups.splice(i, 1)

                                        setStudent({ ...student })
                                    }}
                                    options={allGroups.filter(
                                        (gr) =>
                                            allSelectedGroups.indexOf(gr) ===
                                                -1 || gr === group
                                    )}
                                    selected={group}
                                />
                            </label>
                        ))}
                        {student?.groups?.length !== allGroups.length && (
                            <label className="flex flex-col">
                                <span className="px-1 text-[#616161] font-bold">
                                    Добавить группу
                                </span>
                                <Select
                                    onlyArrow={true}
                                    className="bg-white w-[min-content] h-full"
                                    options={allGroups.filter(
                                        (gr) =>
                                            student?.groups?.indexOf(gr) === -1
                                    )}
                                    onSelected={(val) => {
                                        if (!student) {
                                            return
                                        }

                                        student.groups.push(val)

                                        setStudent({ ...student })
                                    }}
                                />
                            </label>
                        )}
                    </div>
                    <div className="flex gap-4">
                        <Input
                            label="ФИО (родителя)"
                            name="parentFullName"
                            value={student?.parentFullName}
                            onChange={(val) => {
                                if (!student) {
                                    return
                                }

                                student.parentFullName = val

                                setStudent({ ...student })
                            }}
                        />
                        <Input
                            label="Номер телефона родителя"
                            name="parentPhone"
                            value={student?.parentPhone}
                            onChange={(val) => {
                                if (!student) {
                                    return
                                }

                                student.parentPhone = val

                                setStudent({ ...student })
                            }}
                        />
                    </div>
                    <input
                        className="bg-[#5810A1] flex items-center justify-center text-white rounded-2xl py-3 flex-auto max-w-[220px]"
                        type="submit"
                        value="Сохранить изменения"
                    />
                </form>
            </div>
        </div>
    )
}

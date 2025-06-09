import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../../../api'
import { PopUpMenu } from '../../../components/PopUpMenu'
import { Student } from '../../../api/fakeApi'

const keyToLabel: { [k in keyof Student]?: string } = {
    fullName: 'Ученик',
    dateOfBirth: 'Дата рождения',
    groups: 'Группа',
    phone: 'Телефон',
    email: 'Почта',
}

const keys = Object.keys(keyToLabel) as (keyof Student)[]

export function StudentsTable() {
    const [students, setStudents] = useState<Student[]>([])
    const [loaded, setLoaded] = useState(false)
    const [popupOpen, setPopupOpen] = useState<string | number>(-1)
    const navigate = useNavigate()

    useEffect(() => {
        ;(async () => {
            setStudents(await api.students.getAll())
            setLoaded(true)
        })()
    }, [])

    return (
        <div className="w-[100%] h-[100%] overflow-y-scroll">
            <table className="w-[100%] min-w-0 border-separate border-spacing-y-2">
                <thead>
                    <tr>
                        {keys.map((key, i) => (
                            <th
                                className={
                                    (i === 0
                                        ? 'pl-3 font-200 text-black text-[17px]'
                                        : 'text-gray-600') +
                                    ' text-nowrap truncate max-w-[200px] font-normal text-start'
                                }
                                key={key}
                            >
                                {keyToLabel[key]}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {loaded
                        ? students.map((student) => (
                              <tr key={student.id}>
                                  {keys.map((key, i) => (
                                      <td
                                          className={
                                              (i === 0
                                                  ? 'border-l-2 pl-3 rounded-l-xl'
                                                  : '') +
                                              ' text-nowrap border-y-2 max-w-[200px] truncate py-2'
                                          }
                                          key={key}
                                      >
                                          {Array.isArray(student[key])
                                              ? student[key].join(', ')
                                              : student[key]}
                                      </td>
                                  ))}
                                  <td className="border-y-2 py-2 border-r-2 pr-3 rounded-r-xl">
                                      <button
                                          onClick={() =>
                                              setPopupOpen(student.id)
                                          }
                                          className="w-10 h-5 rounded-xl bg-white border hover:bg-gray-200 grid place-items-center transition"
                                      >
                                          <svg
                                              viewBox="0 0 24 24"
                                              fill="currentColor"
                                              className="w-5 h-5 rotate-90"
                                          >
                                              <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" />
                                          </svg>
                                      </button>
                                      <PopUpMenu
                                          className="flex flex-col gap-3"
                                          onClose={() => setPopupOpen(-1)}
                                          open={popupOpen === student.id}
                                      >
                                          <button
                                              onClick={() =>
                                                  navigate(
                                                      '/students/profile/' +
                                                          student.id
                                                  )
                                              }
                                              className="bg-white rounded-xl p-2 border shadow-md"
                                          >
                                              Открыть
                                          </button>
                                          <button className="bg-white rounded-xl p-2 border shadow-md">
                                              Изменить
                                          </button>
                                          <button className="bg-white rounded-xl p-2 border shadow-md">
                                              Удалить
                                          </button>
                                      </PopUpMenu>
                                  </td>
                              </tr>
                          ))
                        : Array.from({ length: 4 }).map((_, i) => (
                              <tr
                                  key={i}
                                  style={{ animationDelay: `${i * 0.1}s` }}
                                  className="bg-gray-300 h-[40px] content-placeholder"
                              >
                                  {Array.from({ length: keys.length + 1 }).map(
                                      (_, i) => (
                                          <td
                                              className={
                                                  (i === 0
                                                      ? 'pl-3 rounded-l-xl font-200'
                                                      : '') +
                                                  (i === keys.length
                                                      ? ' pr-3 rounded-r-xl font-200'
                                                      : '') +
                                                  ' text-nowrap truncate max-w-[200px] font-normal text-start'
                                              }
                                              key={i}
                                          ></td>
                                      )
                                  )}
                              </tr>
                          ))}
                </tbody>
            </table>
        </div>
    )
}

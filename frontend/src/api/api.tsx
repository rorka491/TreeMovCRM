const domain = 'http://127.0.0.1:8000/api/'

type TShudels = {
    org?: string
    title?: string
    start_time?: string
    end_time?: string
    date?: Date
    teacher?: string
    week_day?: string
    classroom?: string
    group?: string
    subject?: string
    is_canceled?: boolean
    is_completed?: boolean
    lesson?: string
    start_date?: Date
    end_date?: Date
}

const isOk = (res: Response): Promise<any> => {
    if (res.ok) {
        return res.json()
    }
    return Promise.reject(`Ошибка ${res.status}`)
}

const getSubjectsRequest = async () => {
    return await fetch(`${domain}schedules/subjects/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => isOk(res))
}

const getClassroomsRequest = async () => {
    return await fetch(`${domain}schedules/classrooms/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => isOk(res))
}

const getShedulesRequest = async (query: TShudels) => {
    return await fetch(`${domain}schedules/classrooms/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(query),
    }).then((res) => isOk(res))
}

const getGroupsRequest = async () => {
    return await fetch(`${domain}schedules/student_groups/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => isOk(res))
}

const getTeachersRequest = async () => {
    return await fetch(`${domain}schedules/teachers/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => isOk(res))
}

const getSearchRequest = async (query: string) => {
    return await fetch(`${domain}schedules/search/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(query),
    }).then((res) => isOk(res))
}

const tokenRequest = async () => {
    return await fetch(`${domain}token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            token: localStorage.getItem('refreshToken'),
        }),
    }).then((res) => isOk(res))
}

export {
    getClassroomsRequest,
    getGroupsRequest,
    getSearchRequest,
    getShedulesRequest,
    getSubjectsRequest,
    getTeachersRequest,
    tokenRequest,
}

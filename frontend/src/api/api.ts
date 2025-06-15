const domain = 'http://127.0.0.1:8000/api/'

export type Schedule = {
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

export const api = {
    isOk(res: Response): Promise<any> {
        if (res.ok) {
            return res.json()
        }
        return Promise.reject(`Ошибка ${res.status}`)
    },

    schedules: {
        async getSubjectsRequest() {
            return await fetch(`${domain}schedules/subjects/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => api.isOk(res))
        },

        async getClassroomsRequest() {
            return await fetch(`${domain}schedules/classrooms/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => api.isOk(res))
        },

        async getShedulesRequest(query: Schedule) {
            return await fetch(`${domain}schedules/classrooms/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(query),
            }).then((res) => api.isOk(res))
        },

        async getGroupsRequest() {
            return await fetch(`${domain}schedules/student_groups/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => api.isOk(res))
        },

        async getTeachersRequest() {
            return await fetch(`${domain}schedules/teachers/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => api.isOk(res))
        },

        async getSearchRequest(query: string) {
            return await fetch(`${domain}schedules/search/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(query),
            }).then((res) => api.isOk(res))
        },

        async tokenRequest() {
            return await fetch(`${domain}token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    token: localStorage.getItem('refreshToken'),
                }),
            }).then((res) => api.isOk(res))
        },
    },
}

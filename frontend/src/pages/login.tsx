import { useState } from 'react'

function Login({ setUser }) {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState<string | null>(null)

    const handleSubmit = (e) => {
        e.preventDefault()
        fetch('/api/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
            credentials: 'include',
        })
            .then((res) => {
                if (!res.ok) throw new Error('Ошибка входа')
                return res.json()
            })
            .then(() => {
                setUser({ username })
            })
            .catch(() => setError('Неверные данные'))
    }

    const styles = {
        container: {
            maxWidth: 320,
            margin: '50px auto',
            padding: 20,
            borderRadius: 10,
            backgroundColor: '#6a0dad', // насыщенный фиолетовый
            boxShadow: '0 0 15px rgba(106, 13, 173, 0.5)',
            color: 'white',
            fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        },
        input: {
            width: '100%',
            padding: '10px 12px',
            marginBottom: 15,
            borderRadius: 6,
            border: 'none',
            fontSize: 16,
            outline: 'none',
        },
        inputLight: {
            backgroundColor: 'white',
            color: '#6a0dad',
            fontWeight: '600',
        },
        button: {
            width: '100%',
            padding: 12,
            borderRadius: 6,
            border: 'none',
            backgroundColor: '#9b30ff', // светлый фиолетовый
            color: 'white',
            fontWeight: '700',
            fontSize: 18,
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
        },
        buttonHover: {
            backgroundColor: '#7a1eea',
        },
        error: {
            marginTop: 10,
            color: '#ff6b6b',
            fontWeight: '600',
            textAlign: 'center',
        },
        title: {
            textAlign: 'center',
            marginBottom: 20,
            fontWeight: '700',
            fontSize: 24,
        },
    }

    // для hover добавим небольшой хук
    const [hover, setHover] = useState(false)

    return (
        <form
            onSubmit={handleSubmit}
            style={styles.container}
            autoComplete="off"
        >
            <div style={styles.title as any}>Вход в систему</div>
            <input
                type="text"
                placeholder="Логин"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{ ...styles.input, ...styles.inputLight }}
            />
            <input
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ ...styles.input, ...styles.inputLight }}
            />
            <button
                type="submit"
                style={
                    hover
                        ? { ...styles.button, ...styles.buttonHover }
                        : styles.button
                }
                onMouseEnter={() => setHover(true)}
                onMouseLeave={() => setHover(false)}
            >
                Войти
            </button>
            {error && <div style={styles.error as any}>{error}</div>}
        </form>
    )
}

export default Login

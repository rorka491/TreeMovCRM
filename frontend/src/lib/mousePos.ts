const mousePos = {
    x: 0,
    y: 0,
}

window.addEventListener('mousemove', (e) => {
    mousePos.x = e.pageX
    mousePos.y = e.pageY
})

export function getMousePos() {
    return { ...mousePos }
}

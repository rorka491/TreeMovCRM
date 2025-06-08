import { useRef, useEffect, useState, useLayoutEffect } from 'react'

export function PopUpMenu({ open, setOpen, onClose, children, className }) {
    const ref = useRef(null)
    const [pos, setPos] = useState({ x: 0, y: 0 })

    useEffect(() => {
        function handleClickOutside(e) {
            if (ref.current && !ref.current.parentNode.contains(e.target)) {
                setOpen?.(false)

                if (open) {
                    onClose?.()
                }
            }
        }

        document.addEventListener('click', handleClickOutside)
        return () => document.removeEventListener('click', handleClickOutside)
    }, [open])

    useLayoutEffect(() => {
        const parent = ref.current?.parentNode

        if (!parent) {
            return
        }

        const selfRect = ref.current.getBoundingClientRect()
        const parentRect = parent.getBoundingClientRect()
        
        selfRect.x = parentRect.left
        selfRect.y = parentRect.bottom

        const selfPosX = Math.min(selfRect.x, window.innerWidth - selfRect.width)
        const selfPosY = Math.min(selfRect.y, window.innerHeight - selfRect.height)
       
        setPos({
            x: selfPosX,
            y: selfPosY
        })
    }, [ref, open])

    return (
        <>
            {open && (
                <div ref={ref} className={className + ` absolute top-[${pos.y}px] left-[${pos.x}px] z-10`}>
                    {children}
                </div>
            )}
        </>
    )
}

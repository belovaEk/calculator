import Header from "../../Header"
import Navigate from "../../Navigate"
import React from "react"

export const Layout = ({ children }: { children: React.ReactNode }) => {
    return (
        <div>
            <Header />
            <main>
                <div className='container'>
                    <Navigate />
                   {children}
                </div>
            </main>
        </div>
    )
}
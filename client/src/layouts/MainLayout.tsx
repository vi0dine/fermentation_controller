import { Fragment } from 'react'
import { Disclosure } from '@headlessui/react'
import { BellIcon, MenuIcon, XIcon } from '@heroicons/react/outline'
import {Link, useLocation} from 'react-router-dom'
import * as _ from 'lodash'

const navigation = ['Dashboard', 'Batches', 'Steps', 'Settings', 'Reports']

function classNames(...classes: string[]) {
    return classes.filter(Boolean).join(' ')
}

type MainLayoutProps = {
    children: JSX.Element
}

const MainLayout = ({children}: MainLayoutProps) => {
    const location = useLocation()

    return (
        <div className="min-h-screen bg-gray-100">
            <div className="bg-indigo-600 pb-32">
                <Disclosure as="nav" className="bg-indigo-600 border-b border-indigo-300 border-opacity-25 lg:border-none">
                    {({ open }) => (
                        <>
                            <div className="max-w-7xl mx-auto px-2 sm:px-4 lg:px-8">
                                <div className="relative h-16 flex items-center justify-between lg:border-b lg:border-indigo-400 lg:border-opacity-25">
                                    <div className="px-2 flex items-center lg:px-0">
                                        <div className="flex-shrink-0">
                                            <img
                                                className="block h-8 w-8"
                                                src="https://tailwindui.com/img/logos/workflow-mark-indigo-300.svg"
                                                alt="Workflow"
                                            />
                                        </div>
                                        <div className="hidden lg:block lg:ml-10">
                                            <div className="flex space-x-4">
                                                {navigation.map((item, itemIdx) => {
                                                    const regexp = new RegExp(`.*${item.toLowerCase()}.*`)
                                                    return location.pathname.match(regexp) ? (
                                                        <Fragment key={item}>
                                                            {/* Current: "bg-indigo-700 text-white", Default: "text-white hover:bg-indigo-500 hover:bg-opacity-75" */}
                                                            <Link to={`/${item.toLowerCase()}`} className="bg-indigo-700 text-white rounded-md py-2 px-3 text-sm font-medium">
                                                                {item}
                                                            </Link>
                                                        </Fragment>
                                                    ) : (
                                                        <Link
                                                            key={item}
                                                            to={`/${item.toLowerCase()}`}
                                                            className="text-white hover:bg-indigo-500 hover:bg-opacity-75 rounded-md py-2 px-3 text-sm font-medium"
                                                        >
                                                            {item}
                                                        </Link>
                                                    )
                                                })}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex lg:hidden">
                                        {/* Mobile menu button */}
                                        <Disclosure.Button className="bg-indigo-600 p-2 rounded-md inline-flex items-center justify-center text-indigo-200 hover:text-white hover:bg-indigo-500 hover:bg-opacity-75 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-indigo-600 focus:ring-white">
                                            <span className="sr-only">Open main menu</span>
                                            {open ? (
                                                <XIcon className="block h-6 w-6" aria-hidden="true" />
                                            ) : (
                                                <MenuIcon className="block h-6 w-6" aria-hidden="true" />
                                            )}
                                        </Disclosure.Button>
                                    </div>
                                    <div className="hidden lg:block lg:ml-4">
                                        <div className="flex items-center">
                                            <button className="bg-indigo-600 flex-shrink-0 rounded-full p-1 text-indigo-200 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-indigo-600 focus:ring-white">
                                                <span className="sr-only">View notifications</span>
                                                <BellIcon className="h-6 w-6" aria-hidden="true" />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <Disclosure.Panel className="lg:hidden">
                                <div className="px-2 pt-2 pb-3 space-y-1">
                                    {navigation.map((item, itemIdx) => {
                                            const regexp = new RegExp(`.*${item.toLowerCase()}.*`)
                                            return location.pathname.match(regexp) ? (
                                                <Fragment key={item}>
                                                    {/* Current: "bg-indigo-700 text-white", Default: "text-white hover:bg-indigo-500 hover:bg-opacity-75" */}
                                                    <Link
                                                        to={`/${item.toLowerCase()}`}
                                                        className="bg-indigo-700 text-white block rounded-md py-2 px-3 text-base font-medium"
                                                    >
                                                        {item}
                                                    </Link>
                                                </Fragment>
                                            ) : (
                                                <Link
                                                    key={item}
                                                    to={`/${item.toLowerCase()}`}
                                                    className="text-white hover:bg-indigo-500 hover:bg-opacity-75 block rounded-md py-2 px-3 text-base font-medium"
                                                >
                                                    {item}
                                                </Link>
                                            )
                                        }
                                    )}
                                </div>
                                <div className="pt-4 pb-3 border-t border-indigo-700">
                                    <div className="px-5 flex items-center">
                                        <div className="flex-shrink-0">
                                            <img
                                                className="rounded-full h-10 w-10"
                                                src="https://www.raspberrypi.org/wp-content/uploads/2011/10/Raspi-PGB001.png"
                                                alt=""
                                            />
                                        </div>
                                        <div className="ml-3">
                                            <div className="text-base font-medium text-white">Brew Valley Link</div>
                                            <div className="text-sm font-medium text-indigo-300">192.168.2.60</div>
                                        </div>
                                        <button className="ml-auto bg-indigo-600 flex-shrink-0 rounded-full p-1 text-indigo-200 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-indigo-600 focus:ring-white">
                                            <span className="sr-only">View notifications</span>
                                            <BellIcon className="h-6 w-6" aria-hidden="true" />
                                        </button>
                                    </div>
                                </div>
                            </Disclosure.Panel>
                        </>
                    )}
                </Disclosure>
                <header className="py-10">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <h1 className="text-3xl font-bold text-white">
                            {_.capitalize(location.pathname.split("/")[1])}
                        </h1>
                    </div>
                </header>
            </div>

            <main className="-mt-32">
                <div className="max-w-7xl mx-auto pb-12 px-4 sm:px-6 lg:px-8">
                    <div className="bg-white rounded-lg shadow px-5 py-6 sm:px-6">
                        {children}
                    </div>
                </div>
            </main>
        </div>
    )
}

export default MainLayout
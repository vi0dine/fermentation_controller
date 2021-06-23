import React, {useEffect, useState} from "react";
import axios from "axios";
import beer from '../../assets/beer.png'
import brewery from '../../assets/brewery.png'
import {AdjustmentsIcon, CheckIcon} from "@heroicons/react/solid";

const Batches = () => {
    const [batches, setBatches] = useState<any>([])

    const fetchBatches = async () => {
        const {data} = await axios.request({
            url: '/batches',
            method: 'GET'
        })

        return data
    };

    const setBatchAsCurrent = async (batch: any) => {
        const {data} = await axios.request({
            url: `/batches/${batch.id}`,
            data: {
                ...batch,
                current: 1
            },
            method: 'PUT'
        })

        setBatches(batches.map((b: any) => {
            if (b.id === batch.id) {
                return {...b, current: 1}
            } else {
                return {...b, current: 0}
            }
        }))

        return data
    };

    useEffect(() => {
        fetchBatches().then(res => {
            setBatches(res || [])
        })
    }, [])

    return <div>
        <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
            {batches.map((batch: any) => (
                <li
                    key={batch.id}
                    className="col-span-1 flex flex-col text-center bg-white rounded-lg shadow divide-y divide-gray-200"
                >
                    <div className="flex-1 flex flex-col p-8">
                        <img className="w-32 h-32 flex-shrink-0 mx-auto bg-transparent rounded-full" src={batch.current ? brewery : beer} alt="" />
                        <h3 className="mt-6 text-gray-900 text-sm font-medium">{batch.name}</h3>
                        <dl className="mt-1 flex-grow flex flex-col justify-between">
                            <dt className="sr-only">Role</dt>
                            <dd className="mt-3">
                                <span className={`px-2 py-1 text-xs font-medium ${batch.current ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-400"} rounded-full`}>
                                  {batch.current ? "Current" : "Archived"}
                                </span>
                            </dd>
                        </dl>
                    </div>
                    <div>
                        <div className="-mt-px flex divide-x divide-gray-200">
                            <div className="w-0 flex-1 flex">
                                <a
                                    className="cursor-pointer relative -mr-px w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-bl-lg hover:text-gray-500"
                                >
                                    <AdjustmentsIcon className="w-5 h-5 text-gray-400" aria-hidden="true" />
                                    <span className="ml-3">Edit</span>
                                </a>
                            </div>
                            <div className="-ml-px w-0 flex-1 flex">
                                <a
                                    onClick={() => setBatchAsCurrent(batch)}
                                    className="cursor-pointer relative w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-br-lg hover:text-gray-500"
                                >
                                    <CheckIcon className="w-5 h-5 text-gray-400" aria-hidden="true" />
                                    <span className="ml-3">Set current</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </li>
            ))}
        </ul>
    </div>
};

export default Batches
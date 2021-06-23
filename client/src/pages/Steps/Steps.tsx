import React, {useEffect, useState} from "react";
import moment from "moment";
import {ClockIcon, FireIcon, CheckIcon} from "@heroicons/react/outline";
import axios from "axios";

function classNames(...classes: string[]) {
    return classes.filter(Boolean).join(' ')
}

const Steps = () => {
    const [steps, setSteps] = useState<any>([])
    const formatStep = (step: any) => {
        const begin = moment.unix(step.begin_date)
        const end = moment.unix(step.end_date)
        const time_difference = begin.diff(end, 'days')+1

        return {
            id: step.id,
            current: step.current,
            content: <p>Keep temperature at <b>{step.temperature}</b> for <b>{time_difference}</b> from <b>{begin.format('LLL')}</b> to <b>{end.format('LLL')}</b>.</p>,
            icon: step.current ? FireIcon : moment().diff(step.end_date) > 0 ? CheckIcon : ClockIcon,
            iconBackground: step.current ? "bg-red-400" : moment().diff(step.end_date) > 0 ? "bg-green-500" : "bg-gray-200",
        }
    }

    const fetchSteps = async () => {
        const {data} = await axios.request({
            url: '/steps',
            method: 'GET'
        })

        return data
    };

    useEffect(() => {
        fetchSteps().then(res => {
            setSteps(res || [])
        })
    }, [])

    const setStepAsCurrent = async (stepId: any) => {
        const step = steps.find((s: any) => s.id === stepId)
        const {data} = await axios.request({
            url: `/steps/${step.id}`,
            data: {
                ...step,
                current: 1
            },
            method: 'PUT'
        })

        setSteps(steps.map((b: any) => {
            if (b.id === step.id) {
                return {...b, current: 1}
            } else {
                return {...b, current: 0}
            }
        }))

        console.log(data)

        return data
    };

    return     <div className="flow-root">
        <ul className="-mb-8">
            {steps.map((step: any) => formatStep(step)).map((step: any, stepIdx: any) => (
                <li key={step.id}>
                    <div className="relative pb-8">
                        {stepIdx !== steps.length - 1 ? (
                            <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                        ) : null}
                        <div className="relative flex space-x-3">
                            <div>
                  <span
                      className={classNames(
                          step.iconBackground,
                          'h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white'
                      )}
                  >
                    <step.icon className="h-5 w-5 text-white" aria-hidden="true" />
                  </span>
                            </div>
                            <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                                <div>
                                    <p className="text-sm text-gray-500">
                                        {step.content}
                                    </p>
                                </div>
                                <div className="text-right text-sm whitespace-nowrap text-gray-500">
                                    <button
                                        onClick={() => setStepAsCurrent(step.id)}
                                        type="button"
                                        className="relative inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                    >
                                        Set as current
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            ))}
        </ul>
    </div>
};

export default Steps
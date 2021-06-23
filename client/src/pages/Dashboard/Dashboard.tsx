import React, {useEffect, useState} from "react";
import * as _ from "lodash"
import axios from "axios";
import TemperatureChart from "./components/TemperatureChart";

const Dashboard = () => {
    const [readings, setReadings] = useState<any>([])
    const [lastTimestamp, setLastTimestamp] = useState(0)

    const fetchReadings = async (lastTimestamp = 0) => {
        const {data} = await axios.request({
            url: '/readings',
            params: {
                last_timestamp: lastTimestamp
            },
            method: 'GET'
        })

        return data
    };

    useEffect(() => {
        fetchReadings().then((res: any[]) => {
            setReadings(res)
            setLastTimestamp(_.last(res)?.time || 0)
        })
    }, [])

    return <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white overflow-hidden shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
                <TemperatureChart data={readings}/>
                <button onClick={() => {
                    fetchReadings(lastTimestamp).then((res: any[]) => {
                        setReadings(res)
                        setLastTimestamp(_.last(res)?.time)
                    })
                }}>Next Page</button>
            </div>
        </div>
    </div>;
};

export default Dashboard;
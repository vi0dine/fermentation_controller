import React from 'react'
import {Axis, Grid, LineSeries, Tooltip, XYChart} from "@visx/xychart";
import moment from "moment";

type TooltipProps = {
    tooltipData: any
    colorScale: any
}

type TemperatureChartProps = {
    data: {
        temperature: number,
        desired: number,
        time: string
    }[]
}

const TemperatureChart = ({data}: TemperatureChartProps) => {
    return <XYChart height={300} xScale={{ type: 'band' }} yScale={{ type: 'linear' }}>
        <Axis orientation="bottom" />
        <Grid columns={false} numTicks={4} />
        <LineSeries dataKey="Readings" data={data} yAccessor={d => d.temperature} xAccessor={d => moment(d.time).format("DD-MM-YY HH:mm:ss")} />
        <LineSeries dataKey="Settings" data={data} yAccessor={d => d.desired} xAccessor={d => moment(d.time).format("DD-MM-YY HH:mm:ss")} />
        <Tooltip
            snapTooltipToDatumX
            snapTooltipToDatumY
            showVerticalCrosshair
            showSeriesGlyphs
            // @ts-ignore
            renderTooltip={({ tooltipData, colorScale }: TooltipProps) => (
                <div>
                    <div style={{ color: colorScale ? colorScale(tooltipData.nearestDatum.key) : '#fff'}}>
                        {tooltipData.nearestDatum.key}
                    </div>
                    {tooltipData.nearestDatum.datum.temperature}
                    {', '}
                    {tooltipData.nearestDatum.datum.desired}
                    {', '}
                    {tooltipData.nearestDatum.datum.time}
                </div>
            )}
        />
    </XYChart>
};

export default TemperatureChart
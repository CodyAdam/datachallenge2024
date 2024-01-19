"use client";
import { StockChartComponent, CandleSeries, Tooltip, Crosshair, Inject, StockChartSeriesCollectionDirective, StockChartSeriesDirective, DateTime, EmaIndicator, RsiIndicator, BollingerBands, LineSeries, TmaIndicator, MomentumIndicator, SmaIndicator, AtrIndicator, Export, AccumulationDistributionIndicator, MacdIndicator, StochasticIndicator } from '@syncfusion/ej2-react-charts';
import { type Data } from '~/lib/data';
import { chartData } from './data';
import { registerLicense } from '@syncfusion/ej2-base';
registerLicense("ORg4AjUWIQA/Gnt2UVhhQlVFfV1dXGtWfFN0QXNddVp4flRDcDwsT3RfQFljSH9ad0NnUH5ZdHdRRg==")
export function Graph({
  data,
}: {
  data: Data;
}) {
  const niceData = data.filter(d=>d.Close_BTC!==null).map((d) => {
    return {
      x: new Date(d.date),
      open: d.Close_BTC!+1,
      high: d.Close_BTC!+2,
      low: d.Close_BTC!-2,
      close: d.Close_BTC,
    };
  });
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b text-black bg-white">
     YO BRO
    <StockChartComponent title='Bitcoin Price' crosshair={{ enable: true, lineType: 'Both'}}
    primaryXAxis={{
      crosshairTooltip: { enable: true }
    }}
    tooltip={{ enable: true }}
    periods={[
      {selected: true, intervalType: 'Hours', interval: 12, text: '12H'}
    ]}
    enablePeriodSelector={false}>
        <StockChartSeriesCollectionDirective>
          <StockChartSeriesDirective type='Candle' dataSource={niceData} xName='x' high='high' low='low' open='open' close='close' name='Apple Inc'>

          </StockChartSeriesDirective>
        </StockChartSeriesCollectionDirective>
        <Inject services={[CandleSeries, DateTime, Tooltip, Crosshair, LineSeries, EmaIndicator, RsiIndicator, BollingerBands, TmaIndicator, MomentumIndicator, SmaIndicator, AtrIndicator, Export, AccumulationDistributionIndicator, MacdIndicator, StochasticIndicator ]} />
     </StockChartComponent>
    </main>
  );
}

package com.example.flink.hourlytips;

import java.util.function.ToDoubleBiFunction;

import com.example.flink.common.datatypes.TaxiFare;

import org.apache.flink.api.common.state.MapState;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.api.common.time.Time;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.TimerService;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;
import org.apache.flink.util.OutputTag;

public class PseudoWindow extends KeyedProcessFunction<Long, TaxiFare, Tuple3<Long, Long, Float>> {

    /**
     *
     */
    private static final long serialVersionUID = 1L;

    private final long durationMsec;

    private transient MapState<Long, Float> sumOfTips;

    private static final OutputTag<TaxiFare> lateFares = new OutputTag<TaxiFare>("lateFares") {

        /**
         *
         */
        private static final long serialVersionUID = 1L;
    };

    public PseudoWindow(org.apache.flink.streaming.api.windowing.time.Time time) {
        this.durationMsec = time.toMilliseconds();
    }

    @Override
    public void open(Configuration conf) throws Exception {
        MapStateDescriptor<Long, Float> sumDesc = new MapStateDescriptor<>("sumOfTips", Long.class, Float.class);
        sumOfTips = getRuntimeContext().getMapState(sumDesc);
    }

    @Override
    public void processElement(TaxiFare fare,
            KeyedProcessFunction<Long, TaxiFare, Tuple3<Long, Long, Float>>.Context ctx,
            Collector<Tuple3<Long, Long, Float>> out) throws Exception {
        
        long eventTime = fare.getEventTime();
        TimerService timerService = ctx.timerService();

        if (eventTime <= timerService.currentWatermark()) {
            
            ctx.output(lateFares, fare);
        
        } else {
            long endOfWindow = (eventTime - (eventTime % durationMsec) + durationMsec -1);
            timerService.registerEventTimeTimer(endOfWindow);
            Float sum = sumOfTips.get(endOfWindow);
            if (sum == null) {
                sum = 0.0F;
            }
            sum += fare.tip;
            sumOfTips.put(endOfWindow, sum);
        }
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext context, Collector<Tuple3<Long, Long, Float>> out) throws Exception {
        long driverId = context.getCurrentKey();
        Float sumOfTips = this.sumOfTips.get(timestamp);
        Tuple3<Long, Long, Float> result = Tuple3.of(driverId, timestamp, sumOfTips);
        out.collect(result);
        this.sumOfTips.remove(timestamp);
    }

}

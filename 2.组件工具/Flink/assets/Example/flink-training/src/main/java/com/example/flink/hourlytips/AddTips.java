package com.example.flink.hourlytips;

import org.apache.flink.api.java.tuple.Tuple3;
import com.example.flink.common.datatypes.TaxiFare;

import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

public class AddTips extends ProcessWindowFunction<TaxiFare, Tuple3<Long, Long, Float>, Long, TimeWindow> {

    /**
     *
     */
    private static final long serialVersionUID = 1L;

    @Override
    public void process(Long key,
            ProcessWindowFunction<TaxiFare, Tuple3<Long, Long, Float>, Long, TimeWindow>.Context context,
            Iterable<TaxiFare> fares, Collector<Tuple3<Long, Long, Float>> out) throws Exception {
        float sumOfTips = 0F;
        for (TaxiFare f: fares) {
            sumOfTips += f.tip;
        }

        out.collect(Tuple3.of(context.window().getEnd(), key, sumOfTips));

    }


}

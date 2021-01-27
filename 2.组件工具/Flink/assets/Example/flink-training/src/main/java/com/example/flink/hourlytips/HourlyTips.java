package com.example.flink.hourlytips;

import com.example.flink.common.datatypes.TaxiFare;
import com.example.flink.common.sources.TaxiFareGenerator;
import com.example.flink.common.utils.ExerciseBase;

import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.util.OutputTag;

public class HourlyTips extends ExerciseBase {

    private static final OutputTag<TaxiFare> lateFares = new OutputTag<TaxiFare>("lateFares") {
        private static final long serialVersionUID = 1L;
    };


    public static void main(String[] args) throws Exception {
    
        StreamExecutionEnvironment env = StreamExecutionEnvironment
            .getExecutionEnvironment();
        env.setParallelism(ExerciseBase.parallelism);

        DataStream<TaxiFare> fares = env.addSource(fareSourceOrTest(new TaxiFareGenerator()));

        // DataStream<Tuple3<Long, Long, Float>> hourlyTips = fares
        //         .keyBy((TaxiFare fare) -> fare.driverId)
        //         .window(TumblingEventTimeWindows.of(Time.hours(1)))
        //         .process(new AddTips());

        SingleOutputStreamOperator hourlyTips = fares
                .keyBy((TaxiFare fare) -> fare.driverId)
                .process(new PseudoWindow(Time.minutes(1)));

        DataStream<Tuple3<Long, Long, Float>> hourlyMax = hourlyTips
            .windowAll(TumblingEventTimeWindows.of(Time.minutes(1)))
            .maxBy(2);

        hourlyTips.getSideOutput(lateFares).print();

        // printOrTest(hourlyMax);

        env.execute("Hourly Tips (java)");

    }
}
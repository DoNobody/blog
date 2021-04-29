package com.example.flink.ridesandfares;

import com.example.flink.common.datatypes.TaxiFare;
import com.example.flink.common.datatypes.TaxiRide;
import com.example.flink.common.sources.TaxiFareGenerator;
import com.example.flink.common.sources.TaxiRideGenerator;
import com.example.flink.common.utils.ExerciseBase;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.co.RichCoFlatMapFunction;
import org.apache.flink.util.Collector;

public class RidesAndFaresExercise extends ExerciseBase {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(ExerciseBase.parallelism);

        DataStream<TaxiRide> rides = env.addSource(rideSourceOrTest(new TaxiRideGenerator()))
                .filter((TaxiRide ride) -> ride.isStart).keyBy((TaxiRide ride) -> ride.rideId);

        DataStream<TaxiFare> fares = env.addSource(fareSourceOrTest(new TaxiFareGenerator()))
                .keyBy((TaxiFare fare) -> fare.rideId);

        DataStream<Tuple2<TaxiRide, TaxiFare>> enrichedRides = rides
                .connect(fares)
                .flatMap(new EnrichmentFunction())
                .uid("enrichment");

        printOrTest(enrichedRides);

        env.execute("Join Rides with Fares (java RichCoFlatMap)");

    }

    public static class EnrichmentFunction
            extends RichCoFlatMapFunction<TaxiRide, TaxiFare, Tuple2<TaxiRide, TaxiFare>> {

        /**
         *
         */
        private static final long serialVersionUID = 1L;

        private ValueState<TaxiRide> rideState;
        private ValueState<TaxiFare> fareState;

        @Override
		public void open(Configuration config) throws Exception {
            rideState = getRuntimeContext().getState(new ValueStateDescriptor<>("saved ride", TaxiRide.class));
            fareState = getRuntimeContext().getState(new ValueStateDescriptor<>("saved fare", TaxiFare.class));

		}
        
        @Override
        public void flatMap1(TaxiRide ride, Collector<Tuple2<TaxiRide, TaxiFare>> out) throws Exception {
            TaxiFare fare = fareState.value();
            if (fare != null) {
                fareState.clear();
                out.collect(Tuple2.of(ride, fare));
            } else {
                rideState.update(ride);
            }
        }

        @Override
        public void flatMap2(TaxiFare fare, Collector<Tuple2<TaxiRide, TaxiFare>> out) throws Exception {
            TaxiRide ride = rideState.value();
            if (ride != null) {
                rideState.clear();
                out.collect(Tuple2.of(ride, fare));
            } else {
                fareState.update(fare);
            }
        }

    }
}

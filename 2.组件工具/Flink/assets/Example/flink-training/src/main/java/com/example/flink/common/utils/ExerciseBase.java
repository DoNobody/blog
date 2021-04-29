package com.example.flink.common.utils;

import com.example.flink.common.datatypes.TaxiFare;
import com.example.flink.common.datatypes.TaxiRide;

import org.apache.flink.streaming.api.functions.sink.SinkFunction;
import org.apache.flink.streaming.api.functions.source.SourceFunction;

/**
 * Base for all exercises with a few helper methods.
 */
public class ExerciseBase {
	public static SourceFunction<TaxiRide> rides = null;
	public static SourceFunction<TaxiFare> fares = null;
	public static SourceFunction<String> strings = null;
	public static SinkFunction out = null;
	public static int parallelism = 4;

	/**
	 * Retrieves a test source during unit tests and the given one during normal execution.
	 */
	public static SourceFunction<TaxiRide> rideSourceOrTest(SourceFunction<TaxiRide> source) {
		if (rides == null) {
			return source;
		}
		return rides;
	}

	/**
	 * Retrieves a test source during unit tests and the given one during normal execution.
	 */
	public static SourceFunction<TaxiFare> fareSourceOrTest(SourceFunction<TaxiFare> source) {
		if (fares == null) {
			return source;
		}
		return fares;
	}

	/**
	 * Retrieves a test source during unit tests and the given one during normal execution.
	 */
	public static SourceFunction<String> stringSourceOrTest(SourceFunction<String> source) {
		if (strings == null) {
			return source;
		}
		return strings;
	}

	/**
	 * Prints the given data stream during normal execution and collects outputs during tests.
	 */
	public static void printOrTest(org.apache.flink.streaming.api.datastream.DataStream<?> ds) {
		if (out == null) {
			ds.print();
		} else {
			ds.addSink(out);
		}
	}
}

package com.example.flink.demo;

import org.apache.flink.api.java.*;
import java.lang.Exception;
import org.apache.flink.api.common.time.Time;
import java.util.concurrent.TimeUnit;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.operators.IterativeDataSet;
import org.apache.flink.api.common.restartstrategy.RestartStrategies;
import org.apache.flink.api.common.time.Time;



public class Demo {
    public static void main(String[] args) throws Exception{
        final ExecutionEnvironment env = ExecutionEnvironment.createLocalEnvironment();
        env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
            3, // 尝试重启的次数
            Time.of(10, TimeUnit.SECONDS)
            ));

        // Create initial IterativeDataSet
        IterativeDataSet<Integer> initial = env.fromElements(0).iterate(100000);

        DataSet<Integer> iteration = initial.map(new MapFunction<Integer, Integer>() {
            @Override
            public Integer map(Integer i) throws Exception {
                double x = Math.random();
                double y = Math.random();

                return i + ((x * x + y * y < 1) ? 1 : 0);
            }
        });

        // Iteratively transform the IterativeDataSet
        initial.closeWith(iteration).map(new MapFunction<Integer, Double>() {
            @Override
            public Double map(Integer count) throws Exception {
                return count / (double) 100000 * 4;
            }
        }).print();

        env.execute("Iterative Pi Example");

    }
}

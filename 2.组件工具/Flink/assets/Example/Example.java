import java.util.ArrayList;
import java.util.List;

import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class Example {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();

        // fromElements 
        // DataStream<Person> flintstones = env.fromElements(
        //         new Person("Fred", 35),
        //         new Person("Wilma", 35),
        //         new Person("Pebbles", 2));

        // fromColletions
        List<Person> people = new ArrayList<Person>();
        people.add(new Person("Fred", 35));
        people.add(new Person("Wilma", 19));
        people.add(new Person("Pebbles", 2));

        DataStream<Person> flintstones = env.fromCollection(people);

        DataStream<Person> adults = flintstones.filter(new FilterFunction<Person>() {
            @Override
            public boolean filter(Person person) throws Exception {
                return person.age >= 18;
            }
        });

        adults.print();

        env.execute();
    }

    public static class Person {
        public String name;
        public Integer age;
        public Person() {};

        public Person(String name, Integer age) {
            this.name = name;
            this.age = age;
        };

        public String toString() {
            return this.name.toString() + ": age " + this.age.toString();
        };
    }
}
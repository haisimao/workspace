package com.hebut.mr; 
 
import java.io.IOException; 
import java.util.StringTokenizer; 
import org.apache.hadoop.conf.Configuration; 
import org.apache.hadoop.fs.Path; 
import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.Text; 
import org.apache.hadoop.mapreduce.Job; 
import org.apache.hadoop.mapreduce.Mapper; 
import org.apache.hadoop.mapreduce.Reducer; 
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat; 
import org.apache.hadoop.mapreduce.lib.input.FileSplit; 
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat; 
import org.apache.hadoop.util.GenericOptionsParser; 
 
public class InvertedIndex 
{ 
 
    public static class Map extends Mapper<Object, Text, Text, Text> 
	{ 
 
        private Text keyInfo = new Text(); // �洢���ʺ�URL���
        private Text valueInfo = new Text(); // �洢��Ƶ
        private FileSplit split; // �洢Split����
 
        // ʵ��map����
        public void map(Object key, Text value, Context context) 
                throws IOException, InterruptedException 
		{ 
 
            // ���<key,value>��������FileSplit����
            split = (FileSplit) context.getInputSplit(); 
 
            StringTokenizer itr = new StringTokenizer(value.toString()); 
 
            while (itr.hasMoreTokens()) 
			{ 
                // keyֵ�ɵ��ʺ�URL��ɣ���"MapReduce��file1.txt"
                // ��ȡ�ļ�������·��
                // keyInfo.set(itr.nextToken()+":"+split.getPath().toString());
                // ����Ϊ�˺ÿ���ֻ��ȡ�ļ������ơ�
                int splitIndex = split.getPath().toString().indexOf("file"); 
                keyInfo.set(itr.nextToken() + ":" + split.getPath().toString().substring(splitIndex)); 
                // ��Ƶ��ʼ��Ϊ1 
                valueInfo.set("1");
                context.write(keyInfo,valueInfo); 
            } 
        } 
    } 
 
    public static class Combine extends Reducer<Text, Text, Text, Text> 
	{ 
 
        private Text info = new Text(); 
 
        // ʵ��reduce����
        public void reduce(Text key, Iterable<Text> values, Context context) 
                throws IOException, InterruptedException 
		{ 
 
            // ͳ�ƴ�Ƶ
            int sum = 0; 
            for (Text value : values) 
			{ 
                sum += Integer.parseInt(value.toString()); 
            } 
 
            int splitIndex = key.toString().indexOf(":"); 
            // ��������valueֵ��URL�ʹ�Ƶ���
            info.set(key.toString().substring(splitIndex + 1) + ":" + sum); 
            // ��������keyֵΪ����
            key.set(key.toString().substring(0, splitIndex)); 
 
            context.write(key,info); 
        } 
    } 
 
    public static class Reduce extends Reducer<Text, Text, Text, Text>
	{ 
 
        private Text result = new Text(); 
 
        // ʵ��reduce����
        public void reduce(Text key, Iterable<Text> values, Context context) 
                throws IOException, InterruptedException 
		{ 
 
            // �����ĵ��б�
            String fileList = new String(); 
            for (Text value : values)
			{ 
                fileList += value.toString() + ";"; 
            } 
 
            result.set(fileList); 
 
            context.write(key,result); 
        } 
    } 
 
    public static void main(String[] args) throws Exception 
	{ 
        Configuration conf = new Configuration(); 
        
 
        
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs(); 
        if (otherArgs.length != 2) 
		{ 
            System.err.println("Usage: Inverted Index <in> <out>"); 
            System.exit(2); 
        } 
 
        Job job = new Job(conf, "Inverted Index"); 
        job.setJarByClass(InvertedIndex.class); 
 
        // ����Map��Combine��Reduce������
        job.setMapperClass(Map.class); 
        job.setCombinerClass(Combine.class); 
        job.setReducerClass(Reduce.class); 
 
        // ����Map�������
        job.setMapOutputKeyClass(Text.class); 
        job.setMapOutputValueClass(Text.class); 
 
        // ����Reduce�������
        job.setOutputKeyClass(Text.class); 
        job.setOutputValueClass(Text.class); 
 
        // ������������Ŀ¼
        FileInputFormat.addInputPath(job, new Path(otherArgs[0])); 
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1])); 
        System.exit(job.waitForCompletion(true) ? 0 : 1); 
    } 
} 

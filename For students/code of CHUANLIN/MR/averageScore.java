package com.hebut.mr; 
 
import java.io.IOException; 
import java.util.Iterator; 
import java.util.StringTokenizer; 
 
import org.apache.hadoop.conf.Configuration; 
import org.apache.hadoop.fs.Path; 
import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.LongWritable; 
import org.apache.hadoop.io.Text; 
import org.apache.hadoop.mapreduce.Job; 
import org.apache.hadoop.mapreduce.Mapper; 
import org.apache.hadoop.mapreduce.Reducer; 
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat; 
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat; 
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat; 
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat; 
import org.apache.hadoop.util.GenericOptionsParser; 
 
public class Score 
{ 
 
    public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> 
	{ 
 
        // ʵ��map����
        public void map(LongWritable key, Text value, Context context) 
                throws IOException, InterruptedException 
		{ 
            // ������Ĵ��ı��ļ�������ת����String 
            String line = value.toString(); 
 
            // ��������������Ȱ��н��зָ�
            StringTokenizer tokenizerArticle = new StringTokenizer(line, "\n"); 
 
            // �ֱ��ÿһ�н��д���
            while (tokenizerArticle.hasMoreElements()) 
			{ 
                // ÿ�а��ո񻮷�
                StringTokenizer tokenizerLine = new StringTokenizer(tokenizerArticle.nextToken()); 
 
                String strName = tokenizerLine.nextToken();// ѧ����������
                String strScore = tokenizerLine.nextToken();// �ɼ�����
 
                Text name = new Text(strName); 
                int scoreInt = Integer.parseInt(strScore); 
                // ��������ͳɼ�
                context.write(name, new IntWritable(scoreInt)); 
            } 
        } 
 
    } 
 
    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable>
	{ 
        // ʵ��reduce����
        public void reduce(Text key, Iterable<IntWritable> values, 
                Context context) throws IOException, InterruptedException 
		{ 
 
            int sum = 0; 
            int count = 0; 
 
            Iterator<IntWritable> iterator = values.iterator(); 
            while (iterator.hasNext()) 
			{ 
                sum += iterator.next().get();// �����ܷ�
                count++;// ͳ���ܵĿ�Ŀ��
            } 
 
            int average = (int) sum / count;// ����ƽ���ɼ�
            context.write(key, new IntWritable(average)); 
        } 
 
    } 
 
    public static void main(String[] args) throws Exception 
	{ 
        Configuration conf = new Configuration(); 
        // ��仰�ܹؼ�
        conf.set("mapred.job.tracker", "192.168.1.2:9001"); 
 
        String[] ioArgs = new String[] { "score_in", "score_out" }; 
        String[] otherArgs = new GenericOptionsParser(conf, ioArgs).getRemainingArgs(); 
        if (otherArgs.length != 2) 
		{ 
            System.err.println("Usage: Score Average <in> <out>"); 
            System.exit(2); 
        } 
 
        Job job = new Job(conf, "Score Average"); 
        job.setJarByClass(Score.class); 
 
        // ����Map��Combine��Reduce������
        job.setMapperClass(Map.class); 
        job.setCombinerClass(Reduce.class); 
        job.setReducerClass(Reduce.class); 
 
        // �����������
        job.setOutputKeyClass(Text.class); 
        job.setOutputValueClass(IntWritable.class); 
 
        // ����������ݼ��ָ��С���ݿ�splites���ṩһ��RecordReder��ʵ��
        job.setInputFormatClass(TextInputFormat.class); 
        // �ṩһ��RecordWriter��ʵ�֣������������
        job.setOutputFormatClass(TextOutputFormat.class); 
 
        // ������������Ŀ¼
        FileInputFormat.addInputPath(job, new Path(otherArgs[0])); 
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1])); 
        System.exit(job.waitForCompletion(true) ? 0 : 1); 
    } 
} 

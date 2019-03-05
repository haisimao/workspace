package recommand.hadoop.phl; 
import java.io.IOException; 
import java.net.URISyntaxException; 
import java.util.Map; 
import org.apache.hadoop.conf.Configuration; 
import org.apache.hadoop.fs.Path; 
import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.Text; 
import org.apache.hadoop.mapreduce.Job; 
import org.apache.hadoop.mapreduce.Mapper; 
import org.apache.hadoop.mapreduce.Reducer; 
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat; 
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat; 
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat; 
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat; 
public class Step1 
{ 
	public static class myMapper extends Mapper<Object,Text,IntWritable,Text> 
	{ 
		private final static IntWritable k = new IntWritable(); 
		private final static Text v = new Text(); 
		@Override 
		protected void map(Object key, Text value, Context context) 
		throws IOException, InterruptedException 
		{ 
			String[] tokens = Recommend.DELIMITER.split(value.toString()); 
			int userID = Integer.parseInt(tokens[0]); 
			String itemID = tokens[1]; 
			String pref = tokens[2]; 
			k.set(userID); 
			v.set(itemID + ":" + pref); 
			context.write(k, v); 
		} 
	} 
	public static class myReducer extends Reducer<IntWritable, Text, IntWritable, Text>
	{ 
		private final static Text v = new Text(); 
		@Override 
		protected void reduce(IntWritable k2, Iterable<Text> v2s,Context context)throws IOException, InterruptedException
		{ 
			StringBuilder sb = new StringBuilder(); 
			for (Text v2 : v2s)
			{ 
				sb.append("," + v2.toString()); 
			} 
			v.set(sb.toString().replaceFirst(",", "")); 
			context.write(k2, v); 
		} 
	} 
	public static void runStep1(Map<String, String> path) throws IOException, URISyntaxException, ClassNotFoundException, InterruptedException 
	{ 
		Configuration conf = new Configuration(); 
        
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs(); 
		if (otherArgs.length != 2) 
		{ 
			System.err.println("Usage: Data Sort <in> <out>"); 
			System.exit(2); 
		} 
		//String input = path.get("Step1Input"); 
		//String output = path.get("Step1Output"); 
		//1.1��ȡhdfs�ļ� 
		Configuration conf = new Configuration(); 
		HDFSDao hdfsDao = new HDFSDao(input,conf,Step1.class.getSimpleName()); 
		Job job = hdfsDao.conf(); 
		//������з��� 
		job.setJarByClass(Step1.class); 
		//1.1��ȡ�ļ� ��������·���Լ��ļ������ʽ 
		//FileInputFormat.addInputPath(job, new Path(input));
		FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
		job.setInputFormatClass(TextInputFormat.class); 
		//ָ���Զ����Mapper�� 
		job.setMapperClass(myMapper.class); 
		//ָ��Mapper�����key value���� 
		job.setMapOutputKeyClass(IntWritable.class); 
		job.setMapOutputValueClass(Text.class); 
		//1.3���� 
		/* job.setPartitionerClass(HashPartitioner.class); 
		job.setNumReduceTasks(1);*/ 
		//1.4���� ���� 
		//1.5��Լ 
		job.setCombinerClass(myReducer.class); 
		//2.1 
		//2.2ָ���Զ����Reduce�� 
		job.setReducerClass(myReducer.class); 
		job.setOutputKeyClass(IntWritable.class); 
		job.setOutputValueClass(Text.class); 
		//2.3ָ�������·�� 
		//FileOutputFormat.setOutputPath(job, new Path(output));
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
		job.setOutputFormatClass(TextOutputFormat.class); 
		hdfsDao.rmr(output); 
		job.waitForCompletion(true); 
	} 
} 
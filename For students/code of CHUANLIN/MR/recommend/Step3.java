package recommand.hadoop.phl;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.Map;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
public class Step3 
{
    public static class myMapper1 extends Mapper<LongWritable, Text, IntWritable, Text>
    {
        private final static IntWritable k = new IntWritable();
        private final static Text v = new Text();
        @Override
        protected void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException 
		{
            //101:101   5
            String[] tokens = Recommend.DELIMITER.split(value.toString());
            for (int i = 1; i < tokens.length; i++)
			{
                String[] vector = tokens[i].split(":");
                int itemID = Integer.parseInt(vector[0]);
                String pref = vector[1];
                k.set(itemID);
                v.set(tokens[0] + ":" + pref);
                context.write(k, v);
            }
        }

    }
        public static class myMapper2 extends Mapper<LongWritable, Text, Text,IntWritable>
    {
         private final static Text k = new Text();
         private final static IntWritable v = new IntWritable();
        @Override
        protected void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException 
		{
            String[] tokens = Recommend.DELIMITER.split(value.toString());
            k.set(tokens[0]);
            v.set(Integer.parseInt(tokens[1]));
            context.write(k, v);
        }
    }
    public static void runStep3_1(Map<String, String> path) throws IOException, URISyntaxException, ClassNotFoundException, InterruptedException
	{
        String input = path.get("Step3Input1");
        String output = path.get("Step3Output1");
        //1.1��ȡhdfs�ļ�
        Configuration conf = new Configuration();
        HDFSDao hdfsDao = new HDFSDao(input,conf,Step3.class.getSimpleName());
        Job job = hdfsDao.conf();
        //������з���
        job.setJarByClass(Step2.class);
        //1.1��ȡ�ļ� ��������·���Լ��ļ������ʽ
        FileInputFormat.addInputPath(job, new Path(input));     
        job.setInputFormatClass(TextInputFormat.class);
        //ָ���Զ����Mapper��
        job.setMapperClass(myMapper1.class);
        //ָ��Mapper�����key value����
        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(Text.class);
        //2.3ָ�������·��
        FileOutputFormat.setOutputPath(job, new Path(output));
        job.setOutputFormatClass(TextOutputFormat.class);
        //����Ƿ�������ͬ���������ɾ��  
        hdfsDao.rmr(output);
        job.waitForCompletion(true);
    }

    public static void runStep3_2(Map<String, String> path) throws IOException, URISyntaxException, ClassNotFoundException, InterruptedException
	{
        String input = path.get("Step3Input2");
        String output = path.get("Step3Output2");
        //1.1��ȡhdfs�ļ�
        Configuration conf = new Configuration();
        HDFSDao hdfsDao = new HDFSDao(input,conf,Step3.class.getSimpleName());
        Job job = hdfsDao.conf();
        //������з���
        job.setJarByClass(Step2.class);
        //1.1��ȡ�ļ� ��������·���Լ��ļ������ʽ
        FileInputFormat.addInputPath(job, new Path(input));     
        job.setInputFormatClass(TextInputFormat.class);
        //ָ���Զ����Mapper��
        job.setMapperClass(myMapper2.class);
        //ָ��Mapper�����key value����
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        //2.3ָ�������·��
        FileOutputFormat.setOutputPath(job, new Path(output));
        job.setOutputFormatClass(TextOutputFormat.class);
        //����Ƿ�������ͬ���������ɾ��  
        hdfsDao.rmr(output);
        job.waitForCompletion(true);
	}
}
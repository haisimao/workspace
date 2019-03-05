package recommand.hadoop.phl;

import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

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

import recommand.hadoop.phl.Step1.myReducer;

public class Step4
{
    public static class myMapper extends Mapper<LongWritable, Text, IntWritable, Text>
	{
		private final static IntWritable k = new IntWritable();
		private final static Text v = new Text();
		private final static Map<Integer, List> cooccurrenceMatrix = new HashMap<Integer, List>();
		@Override
		protected void map(LongWritable key, Text values, Mapper<LongWritable, Text, IntWritable, Text>.Context context)
				throws IOException, InterruptedException 
		{
			String[] tokens = Recommend.DELIMITER.split(values.toString());

			//同现矩阵时候，v1存的是101 101，v2存的是5。用户评分矩阵，v1存的是101 v2存的是1 5.0
			String[] v1 = tokens[0].split(":");
			String[] v2 = tokens[1].split(":"); 

			if (v1.length > 1) 
			{// cooccurrence
				int itemID1 = Integer.parseInt(v1[0]);
				int itemID2 = Integer.parseInt(v1[1]);
				int num = Integer.parseInt(tokens[1]);

				List<Cooccurrence> list = null;
				if (!cooccurrenceMatrix.containsKey(itemID1)) 
				{
					list = new ArrayList<Cooccurrence>();
				} 
				else 
				{
					list = cooccurrenceMatrix.get(itemID1);
				}
				list.add(new Cooccurrence(itemID1, itemID2, num));
				System.out.println("<itemID1,{itemID1, itemID2, num}: "+itemID1+"{"+itemID1+" , "+itemID2+" , "+num+"}");
				cooccurrenceMatrix.put(itemID1, list);
			}

			if (v2.length > 1) 
			{// userVector
				int itemID = Integer.parseInt(tokens[0]);
				int userID = Integer.parseInt(v2[0]);
				double pref = Double.parseDouble(v2[1]);
				k.set(userID);

				Iterator<Cooccurrence> iterator = cooccurrenceMatrix.get(itemID).iterator();
				while(iterator.hasNext())
				{
					Cooccurrence co = iterator.next();
					v.set(co.getItemID2() + "," + pref * co.getNum());
					System.out.println("ItemID2,pref * co.getNum()"+userID+":{"+co.getItemID2()+ "," + pref * co.getNum()+"}");
					context.write(k, v);
				}

					/*for (Cooccurrence co : cooccurrenceMatrix.get(itemID)) {
						v.set(co.getItemID2() + "," + pref * co.getNum());
						context.write(k, v);
					}*/
			}
		}
    }
    public static class myReducer extends Reducer<IntWritable, Text, IntWritable, Text>
	{
        private final static Text v = new Text();
        @Override
        protected void reduce(IntWritable key, Iterable<Text> values,
                Context context)throws IOException, InterruptedException 
		{
            Map<String, Double> result = new HashMap<String, Double>();
            for(Text value:values)
			{
                String[] str = value.toString().split(",");
                if (result.containsKey(str[0])) 
				{
                    result.put(str[0], result.get(str[0]) + Double.parseDouble(str[1]));
                }
				else
				{
                    result.put(str[0], Double.parseDouble(str[1]));
                }
            }
            Iterator iter = result.keySet().iterator();
            while (iter.hasNext()) 
			{
                String itemID = iter.next().toString();
                System.out.println("itemID:"+itemID);
                double score = result.get(itemID);
                v.set(itemID + "," + score);
                context.write(key, v);
            }
        }
    }

    public static void runStep4(Map<String, String> path) throws IOException, URISyntaxException, ClassNotFoundException, InterruptedException 
	{
        String input1 = path.get("Step4Input1");
        String input2 = path.get("Step4Input2");
        String output = path.get("Step4Output");
        //1.1读取hdfs文件
        Configuration conf = new Configuration();
        HDFSDao hdfsDao = new HDFSDao(conf,Step1.class.getSimpleName());
        Job job = hdfsDao.conf();
        //打包运行方法
        job.setJarByClass(Step1.class);
        //1.1读取文件 设置输入路径以及文件输入格式
        FileInputFormat.setInputPaths(job, new Path(input1), new Path(input2));     
        job.setInputFormatClass(TextInputFormat.class);
        //指定自定义的Mapper类
        job.setMapperClass(myMapper.class);
        //指定Mapper输出的key value类型
        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(Text.class);

        //2.2指定自定义的Reduce类
        job.setReducerClass(myReducer.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);
        //2.3指定输出的路径
        FileOutputFormat.setOutputPath(job, new Path(output));
        job.setOutputFormatClass(TextOutputFormat.class);
        hdfsDao.rmr(output);
        job.waitForCompletion(true);
    }
}
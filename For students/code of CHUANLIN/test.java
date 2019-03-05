import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
public class HDFSTestEx 
{
	public static void main(String[] args)
	{
		try
		{
			String fileName="hdfs://localhost:9000/user/hduser/hfile";
			Configuration conf=new Configuration();
			conf.set("fs.default.name", "hdfs://localhost:9000");
			FileSystem fs=FileSystem.get(conf);
			if(fs.exists(new Path(fileName)))
			{
				System.out.println("File existed!");
			}
			else
			{
				System.out.println("File dose not exists!");
			}
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}
}
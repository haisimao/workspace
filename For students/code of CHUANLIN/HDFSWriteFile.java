import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.Path;
public class HDFSWriteFile
{
	public static void main(String[] args)
	{
		try
		{
			Configuration conf= new Configuration();
			Path dfs=new Path("hdfs://localhost:9000/");
			FileSystem fs=dfs.getFileSystem(conf);
			byte[] buff="Hello world".getBytes();
			String filename="hdfs://localhost:9000/user/hadoop/test.txt";
			FSDataOutputStream os=fs.create(new Path(filename));
		    os.write(buff, 2, buff.length-2);
		    System.out.println("Create:"+filename);	
		    os.close();
		    fs.close();
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}
}




import java.io.BufferedReader;
import java.io.InputStreamReader;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class LocalFile2Hdfs
{
	public static void main(String[] args)
	{
		try
		{
				Configuration conf = new Configuration();
				 Path dfs=new Path("hdfs://localhost:9000/");
		         FileSystem fs=dfs.getFileSystem(conf);
				Path src= new Path("/home/hduser/localTempfile");
				Path dst=new Path("hdfs://localhost:9000/user/hduser");
				fs.copyFromLocalFile(src, dst);
				
				byte[] buff="Hello HDFS, I wanna to  input anything I want!".getBytes();
				String filename="hdfs://localhost:9000/user/hduser/localTempfile";
				FSDataOutputStream os=fs.create(new Path(filename));
			    os.write(buff,  2, buff.length-4);
			    System.out.println("Create:"+filename);	
			   fs.close();
			    
			   FileSystem fsRead=dfs.getFileSystem(conf);
			    Path filenameRead=new Path("hdfs://localhost:9000/user/hduser/localTempfile");
			    FSDataInputStream is = fsRead.open(filenameRead);         
		        BufferedReader d = new BufferedReader(new InputStreamReader(is));
		        String content = d.readLine(); //读取文件一行 
		        System.out.println(content);
		        d.close(); //关闭文件 
		       
		        Path srcHd=new Path("hdfs://localhost:9000/user/hduser/localTempfile");
		        Path dstLocal=new Path("/home/hduser/newfile");
		        fsRead.copyToLocalFile(srcHd, dstLocal);
		        fsRead.close();
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
    }
}
